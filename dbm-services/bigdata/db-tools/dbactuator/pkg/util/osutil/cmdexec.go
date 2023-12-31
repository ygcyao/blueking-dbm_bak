package osutil

import (
	"bytes"
	"fmt"
	"os"
	"os/exec"
	"strings"
	"syscall"

	"github.com/golang/glog"
	"github.com/pkg/errors"
)

// FileOutputCmd 封装exec.Command，用于执行命令并输出到文件的场景，支持自动将输出文件上传到文件服务器(尽可能上传，如果上传失败则返回原文件)
type FileOutputCmd struct {
	exec.Cmd
	StdOutFile string
	StdErrFile string

	stdOutFile         *os.File
	stdErrFile         *os.File
	stdOutDownloadLink string
	stdErrDownloadLink string
}

// GetStdOutDownloadLink TODO
func (c *FileOutputCmd) GetStdOutDownloadLink() string {
	return c.stdOutDownloadLink
}

// GetStdErrDownloadLink TODO
func (c *FileOutputCmd) GetStdErrDownloadLink() string {
	return c.stdErrDownloadLink
}

func (c *FileOutputCmd) initOutputFile() error {
	if c.StdErrFile == "" {
		c.StdErrFile = c.StdOutFile
	}
	if c.StdOutFile != "" {
		stdOutFile, err := os.OpenFile(c.StdOutFile, os.O_CREATE|os.O_WRONLY, os.ModePerm)
		if err != nil {
			return errors.Wrapf(err, "open std out log file %s failed", c.StdOutFile)
		}
		c.stdOutFile = stdOutFile
		c.Cmd.Stdout = stdOutFile
	}

	if c.StdOutFile == c.StdErrFile {
		c.stdErrFile = nil
		c.Cmd.Stderr = c.stdOutFile
		return nil
	}

	if c.StdErrFile != "" {
		stdErrFile, err := os.OpenFile(c.StdErrFile, os.O_CREATE|os.O_WRONLY, os.ModePerm)
		if err != nil {
			return errors.Wrapf(err, "open std err log file %s failed", c.StdErrFile)
		}
		c.stdErrFile = stdErrFile
		c.Cmd.Stderr = stdErrFile
	}
	return nil
}

func (c *FileOutputCmd) closeOutputFile() {
	if c.stdOutFile != nil {
		if err := c.stdOutFile.Close(); err != nil {
			glog.Warning("close %s failed, err:%s", c.StdOutFile, err.Error())
		}
	}
	if c.stdErrFile != nil {
		if err := c.stdErrFile.Close(); err != nil {
			glog.Warning("close %s failed, err:%s", c.StdErrFile, err.Error())
		}
	}
	// UploadPath?
	return
}

// Run TODO
func (c *FileOutputCmd) Run() error {
	if err := c.initOutputFile(); err != nil {
		return err
	}

	defer func() {
		c.closeOutputFile()
	}()

	return c.Cmd.Run()
}

// Start TODO
func (c *FileOutputCmd) Start() error {
	if err := c.initOutputFile(); err != nil {
		return err
	}

	return c.Cmd.Start()
}

// Wait TODO
func (c *FileOutputCmd) Wait() error {
	defer func() {
		c.closeOutputFile()
	}()

	return c.Cmd.Wait()
}

// RunInBG TODO
func RunInBG(isSudo bool, param string) (pid int, err error) {
	if isSudo {
		param = "sudo " + param
	}
	cmd := exec.Command("bash", "-c", param)
	err = cmd.Start()
	if err != nil {
		return -1, err
	}
	return cmd.Process.Pid, nil
}

// ExecShellCommand 执行 shell 命令
// 如果有 err, 返回 stderr; 如果没有 err 返回的是 stdout
func ExecShellCommand(isSudo bool, param string) (stdoutStr string, err error) {
	if isSudo {
		param = "sudo " + param
	}
	cmd := exec.Command("bash", "-c", param)

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err = cmd.Run()
	if err != nil {
		// return stderr.String(), err
		return stderr.String(), errors.WithMessage(err, stderr.String())
	}
	if len(stderr.String()) > 0 {
		err = fmt.Errorf("execute shell command(%s) error:%s", param, stderr.String())
		return stderr.String(), err
	}
	return stdout.String(), nil
}

// CleanExecShellOutput TODO
func CleanExecShellOutput(s string) string {
	return strings.ReplaceAll(strings.TrimSpace(s), "\n", "")
}

// ExecShellCommandBd 执行 shell 命令
// 大数据部分命令行工具，无法通过err是否为空来判断执行的结果
// 区分stdout,stderr,返回exit code
func ExecShellCommandBd(isSudo bool, param string) (stdoutStr string, stderrStr string, exitCode int) {
	defaultFailedCode := 1

	if isSudo {
		param = "sudo " + param
	}
	cmd := exec.Command("bash", "-c", param)

	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	stdoutStr = stdout.String()
	stderrStr = stderr.String()

	if err != nil {
		// try to get the exit code
		if exitError, ok := err.(*exec.ExitError); ok {
			ws := exitError.Sys().(syscall.WaitStatus)
			exitCode = ws.ExitStatus()
		} else {
			// This will happen (in OSX) if `name` is not available in $PATH,
			// in this situation, exit code could not be get, and stderr will be
			// empty string very likely, so we use the default fail code, and format err
			// to string and set to stderr
			exitCode = defaultFailedCode
			if stderrStr == "" {
				stderrStr = err.Error()
			}
		}
	} else {
		// success, exitCode should be 0 if go is ok
		ws := cmd.ProcessState.Sys().(syscall.WaitStatus)
		exitCode = ws.ExitStatus()
	}
	return stdoutStr, stderrStr, exitCode
}
