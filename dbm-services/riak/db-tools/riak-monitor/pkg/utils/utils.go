// Package utils TODO
package utils

import (
	"bytes"
	"fmt"
	"net"
	"os/exec"

	"github.com/pkg/errors"
)

// ExecShellCommand 执行 shell 命令
// 如果有 err, 返回 stderr; 如果没有 err 返回的是 stdout
// 后续尽量不要用这个方法,因为通过标准错误来判断有点不靠谱
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
		if len(stderr.String()) > 0 {
			return stderr.String(), errors.WithMessage(err, stderr.String())
		} else {
			return stdout.String(), errors.WithMessage(err, stderr.String())
		}
	}

	if len(stderr.String()) > 0 {
		err = fmt.Errorf("execute shell command(%s) error:%s", param, stderr.String())
		return stderr.String(), err
	}

	return stdout.String(), nil
}

// GetLocalIP 获得本地IP
func GetLocalIP() (string, error) {
	var localIP string
	var err error
	addrs, err := net.InterfaceAddrs()
	if err != nil {
		return localIP, err
	}
	for _, addr := range addrs {
		if ipnet, ok := addr.(*net.IPNet); ok && !ipnet.IP.IsLoopback() {
			if ipnet.IP.To4() != nil {
				localIP = ipnet.IP.String()
				return localIP, nil
			}
		}
	}
	err = fmt.Errorf("can't find local ip")
	return localIP, err
}
