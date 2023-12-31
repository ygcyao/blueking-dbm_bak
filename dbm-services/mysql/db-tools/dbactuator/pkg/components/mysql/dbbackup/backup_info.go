package dbbackup

import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"

	"dbm-services/common/go-pubpkg/cmutil"
	"dbm-services/mysql/db-tools/dbactuator/pkg/components/mysql/common"
	"dbm-services/mysql/db-tools/dbactuator/pkg/core/cst"
	"dbm-services/mysql/db-tools/dbactuator/pkg/util"
	"dbm-services/mysql/db-tools/dbactuator/pkg/util/osutil"

	"github.com/pkg/errors"
)

// BackupFile TODO
type BackupFile struct {
	Filename string    `json:"filename"`
	FileInfo *FileInfo `json:"file_info"`
}

// FileInfo TODO
type FileInfo struct {
	Md5           string `json:"md5"`
	Size          string `json:"size"`
	CreateTime    string `json:"createTime"`
	FileLastMtime string `json:"file_last_mtime"`
	SourceIp      string `json:"source_ip"`
	SourcePort    string `json:"source_port"`
}

// InfoFileDetail save info in the MYSQL_FULL_BACKUP .info file
type InfoFileDetail struct {
	App        string            `json:"app"`
	Charset    string            `json:"charset"`
	DbList     []string          `json:"dbList"`
	Cmd        string            `json:"cmd"`
	BackupType string            `json:"backupType"`
	BackupRole string            `json:"backupRole"`
	FileInfo   map[string]string `json:"fileInfo"` // {"somefile.tar":"md5_value", "file": "md5"}
	FullyStamp string            `json:"fullyStamp"`
	FullName   string            `json:"fullName"`
	BackupHost string
	BackupPort int
	StartTime  string

	flagTar        bool
	backupBasename string

	infoFilePath string // InfoFileDetail full path filename
	fileList     []BackupFile
	// backupFiles, full: [], info:[], priv:[]
	backupFiles map[string][]string

	backupDir string // 备份所在目录
	targetDir string
}

// ParseBackupInfoFile 读取 .info 文件
// infoFile 输入完整路径
func ParseBackupInfoFile(infoFilePath string, infoObj *InfoFileDetail) error {
	// func (i *InfoFileDetail) Load(infoFile string) error {
	fileDir, fileName := filepath.Split(infoFilePath)
	f, err := os.Open(infoFilePath)
	if err != nil {
		return errors.Wrap(err, infoFilePath) // os.IsNotExist(err) || os.IsPermission(err)
	}
	defer f.Close()

	scanner := bufio.NewScanner(f)
	reg := regexp.MustCompile(`^(\w+)\s*=\s*(.*)$`)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		array := reg.FindStringSubmatch(line)
		if len(array) != 3 {
			continue
		}
		k, v := array[1], array[2]

		switch k {
		case "APP":
			infoObj.App = v
		case "CHARSET":
			infoObj.Charset = v
		case "DBLIST":
			dblist := util.SplitAnyRune(v, " ")
			dblist = util.RemoveEmpty(dblist)
			infoObj.DbList = dblist
		case "CMD":
			infoObj.Cmd = v
		case "BACKTYPE":
			infoObj.BackupType = common.LooseBackupTypeMap(v)
			if util.StringsHasICase(common.LooseBackupTypeList(), v) {
				infoObj.flagTar = true
			}
		case "BACKROLE":
			infoObj.BackupRole = v
		case "FILE_INFO":
			res := make([]map[string]string, 0)
			if err := json.Unmarshal([]byte(v), &res); err != nil {
				return fmt.Errorf("unmarshal file info failed, data:%s, err:%s", v, err.Error())
			}
			fileMap := make(map[string]string)
			for _, row := range res {
				for k, v := range row {
					fileMap[k] = v
				}
			}
			infoObj.FileInfo = fileMap
		case "FULLY_STAMP":
			infoObj.FullyStamp = v
		case "FULLY_NAME":
			infoObj.FullName = v
		default:
		}
	}
	if err := scanner.Err(); err != nil {
		return fmt.Errorf("scan file %s failed, err:%s", infoFilePath, err.Error())
	}
	if err := infoObj.parseBackupInstance(); err != nil {
		return err
	}
	infoObj.infoFilePath = infoFilePath
	infoObj.backupBasename = strings.TrimSuffix(fileName, ".info")
	infoObj.backupDir = fileDir
	// infoObj.targetDir = filepath.Join(fileDir, infoObj.backupIndexBasename)
	if err := infoObj.getFullFileListFromInfo(false); err != nil {
		return err
	}
	return infoObj.ValidateFiles()
}

// parseBackupInstance 从 cmd 中过去 backupHost, backupPort, startTime
func (i *InfoFileDetail) parseBackupInstance() error {
	var reg *regexp.Regexp
	if i.BackupType == cst.TypeGZTAB {
		// --gztab=/data1/dbbak/DBHA_host-1_127.0.0.1_20000_20220831_200425
		reg = regexp.MustCompile(`gztab=.*_(\d+\.\d+\.\d+\.\d+)_(\d+)_(\d+_\d+).*`)
	} else if i.BackupType == cst.TypeXTRA {
		// --target-dir=/data1/dbbak/DBHA_host-1_127.0.0.1_20000_20220907_040332_xtra
		reg = regexp.MustCompile(`target-dir=.*_(\d+\.\d+\.\d+\.\d+)_(\d+)_(\d+_\d+).*`)
	} else {
		return fmt.Errorf("uknown backup type %s", i.BackupType)
	}
	m := reg.FindStringSubmatch(i.Cmd)
	if len(m) != 4 {
		return fmt.Errorf("failed to get host:port from %s", i.Cmd)
	}
	i.BackupHost = m[1]
	i.BackupPort, _ = strconv.Atoi(m[2])
	timeLayout := `20060102_150405`
	timeLayoutNew := `2006-01-02 15:04:05`
	if t, e := time.Parse(timeLayout, m[3]); e != nil {
		return fmt.Errorf("backup start_time parse failed %s", m[3])
	} else {
		i.StartTime = t.Format(timeLayoutNew)
	}
	return nil
}

// ValidateFiles godoc
// 如果给了 .info ，以 .info 文件为准
// 执行完后，fullFileList 会有排好序的全备文件名，BackupFiles[MYSQL_FULL_BACKUP] 里有全部文件对应的信息
// full 会校验它的连续性
func (i *InfoFileDetail) ValidateFiles() error {
	var errFiles []string

	// BackupFiles[MYSQL_FULL_BACKUP] 可能来自参数传递，也可能来自 .info 里面读取
	fullFileList := i.backupFiles[MYSQL_FULL_BACKUP]
	if len(fullFileList) == 0 {
		return fmt.Errorf("expect more than one full file but got %v", fullFileList)
	} else if len(fullFileList) >= 2 { // 校验文件是否连续
		fileSeqList := util.GetSuffixWithLenAndSep(fullFileList, ".", 0)
		if err := util.IsConsecutiveStrings(fileSeqList, true); err != nil {
			return err
		}
	}

	// 校验文件是否存在
	// 简单校验文件大小。文件md5应该是下载完就要保证一致的，所以这里不校验
	for _, f := range fullFileList {
		if cmutil.GetFileSize(filepath.Join(i.backupDir, f)) < 0 {
			errFiles = append(errFiles, f)
		}
	}
	if len(errFiles) > 0 {
		return errors.Errorf("error files: %v", errFiles)
	}
	return nil
}

// getFullFileListFromInfo 从 .info 里面获取全备文件名
// 会解析 infoFile
func (i *InfoFileDetail) getFullFileListFromInfo(checkMD5 bool) error {

	var fullFiles []BackupFile // @todo md5这里校验，不用传到外面，移除
	var fullFileNames []string
	for fname, fmd5 := range i.FileInfo {
		f := BackupFile{Filename: fname, FileInfo: &FileInfo{Md5: fmd5}}
		fullFiles = append(fullFiles, f)
		fullFileNames = append(fullFileNames, fname)
	}
	if len(fullFiles) == 0 {
		return errors.New("full files not found")
	}
	i.backupFiles[MYSQL_FULL_BACKUP] = fullFileNames
	// sort.Strings(fullFileList)
	return nil
}

// UntarFiles merge and untar
// set targetDir
// 解压到哪个目录，比如 untarDir = /data1/dbbak，解压完后 targetDir = /data1/dbbak/xxx_xxx_xxx/
func (i *InfoFileDetail) UntarFiles(untarDir string) error {
	// 检查磁盘空间大小

	// cat aa.0 aa.1 | tar -xf - -C workdir/
	var cmd string
	if untarDir == "" {
		return errors.Errorf("untar target dir should not be emtpy")
	}
	i.targetDir = filepath.Join(untarDir, i.backupBasename)

	if cmutil.FileExists(i.targetDir) {
		return errors.Errorf("target untar path already exists %s", i.targetDir)
	}
	fullFileList := i.backupFiles[MYSQL_FULL_BACKUP]

	if len(fullFileList) >= 2 {
		cmd = fmt.Sprintf(
			`cd %s && cat %s | tar -xf - -C %s/`,
			i.backupDir, strings.Join(fullFileList, " "), untarDir,
		)
	} else {
		cmd = fmt.Sprintf(
			`cd %s && tar -xf %s -C %s/`,
			i.backupDir, strings.Join(fullFileList, " "), untarDir,
		)
	}
	if _, err := osutil.ExecShellCommand(false, cmd); err != nil {
		return errors.Wrap(err, cmd)
	}
	if !cmutil.FileExists(i.targetDir) {
		return errors.Errorf("targetDir %s is not ready", i.targetDir)
	}
	return nil
}

func (i *InfoFileDetail) GetMetafileBasename() string {
	return i.backupBasename
}
