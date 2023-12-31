/*
 * TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
 * Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at https://opensource.org/licenses/MIT
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 */

package handler

import (
	"os"
	"path"
	"strings"

	"dbm-services/common/go-pubpkg/cmutil"
	"dbm-services/common/go-pubpkg/logger"
	"dbm-services/mysql/db-simulation/app"
	"dbm-services/mysql/db-simulation/app/syntax"

	"github.com/gin-gonic/gin"
	"github.com/spf13/viper"
)

var tmysqlParserBin string
var workdir string

func init() {
	tmysqlParserBin = strings.TrimSpace(viper.GetString("tmysqlparser_bin"))
	// 容器环境会把 tmysqlparse 打包进来
	// 放到和 svr 程序一个目录下
	// 所以在使用这个工程的 img 时, 可以不用设置这个 env
	if len(tmysqlParserBin) == 0 {
		tmysqlParserBin = "/tmysqlparse"
	}
	workdir = strings.TrimSpace(viper.GetString("workdir"))
	if workdir == "" {
		workdir = "/tmp"
	}
}

// SyntaxHandler TODO
type SyntaxHandler struct{}

// CheckSqlStringParam TODO
type CheckSqlStringParam struct {
	ClusterType string   `json:"cluster_type" binding:"required"`
	Version     string   `json:"version"`
	Sqls        []string `json:"sqls" binding:"gt=0,dive,required"`
}

// SyntaxCheckSQL TODO
func SyntaxCheckSQL(r *gin.Context) {
	requestId := r.GetString("request_id")
	var param CheckSqlStringParam
	// 将request中的数据按照json格式直接解析到结构体中
	if err := r.ShouldBindJSON(&param); err != nil {
		logger.Error("ShouldBind failed %s", err)
		SendResponse(r, err, nil, requestId)
		return
	}
	sqlContext := strings.Join(param.Sqls, "\n")
	fileName := "ce_" + cmutil.RandStr(10) + ".sql"
	f := path.Join(workdir, fileName)
	err := os.WriteFile(f, []byte(sqlContext), 0666)
	if err != nil {
		SendResponse(r, err, err.Error(), requestId)
		return
	}
	check := &syntax.TmysqlParseFile{
		TmysqlParse: syntax.TmysqlParse{
			TmysqlParseBinPath: tmysqlParserBin,
			BaseWorkdir:        workdir,
		},
		IsLocalFile: true,
		Param: syntax.CheckSqlFileParam{
			BkRepoBasePath: "",
			FileNames:      []string{fileName},
			MysqlVersion:   param.Version,
		},
	}
	var data map[string]*syntax.CheckInfo
	logger.Info("cluster type :%s", param.ClusterType)
	switch strings.ToLower(param.ClusterType) {
	case app.Spider, app.TendbCluster:
		data, err = check.Do(app.Spider)
	case app.MySQL:
		data, err = check.Do(app.MySQL)
	default:
		data, err = check.Do(app.MySQL)
	}

	if err != nil {
		SendResponse(r, err, data, requestId)
		return
	}
	SendResponse(r, nil, data, requestId)
}

// CheckFileParam TODO
type CheckFileParam struct {
	ClusterType string   `json:"cluster_type"`
	Path        string   `json:"path" binding:"required"`
	Version     string   `json:"version"`
	Files       []string `json:"files" binding:"gt=0,dive,required"`
}

// SyntaxCheckFile 运行语法检查
//
//	@receiver s
//	@param r
func SyntaxCheckFile(r *gin.Context) {
	requestId := r.GetString("request_id")
	var param CheckFileParam
	// 将request中的数据按照json格式直接解析到结构体中
	if err := r.ShouldBindJSON(&param); err != nil {
		logger.Error("ShouldBind failed %s", err)
		SendResponse(r, err, nil, requestId)
		return
	}
	check := &syntax.TmysqlParseFile{
		TmysqlParse: syntax.TmysqlParse{
			TmysqlParseBinPath: tmysqlParserBin,
			BaseWorkdir:        workdir,
		},
		Param: syntax.CheckSqlFileParam{
			BkRepoBasePath: param.Path,
			FileNames:      param.Files,
			MysqlVersion:   param.Version,
		},
	}
	var data map[string]*syntax.CheckInfo
	var err error
	logger.Info("cluster type :%s", param.ClusterType)
	switch strings.ToLower(param.ClusterType) {
	case app.Spider, app.TendbCluster:
		data, err = check.Do(app.Spider)
	case app.MySQL:
		data, err = check.Do(app.MySQL)
	default:
		data, err = check.Do(app.MySQL)
	}

	if err != nil {
		SendResponse(r, err, data, requestId)
		return
	}
	SendResponse(r, nil, data, requestId)
}

// CreateAndUploadDDLTblListFile TODO
func CreateAndUploadDDLTblListFile(r *gin.Context) {
	requestId := r.GetString("request_id")
	var param CheckFileParam
	// 将request中的数据按照json格式直接解析到结构体中
	if err := r.ShouldBindJSON(&param); err != nil {
		logger.Error("ShouldBind failed %s", err)
		SendResponse(r, err, nil, requestId)
		return
	}
	check := &syntax.TmysqlParseFile{
		TmysqlParse: syntax.TmysqlParse{
			TmysqlParseBinPath: tmysqlParserBin,
			BaseWorkdir:        workdir,
		},
		Param: syntax.CheckSqlFileParam{
			BkRepoBasePath: param.Path,
			FileNames:      param.Files,
			MysqlVersion:   param.Version,
		},
	}
	if err := check.CreateAndUploadDDLTblFile(); err != nil {
		SendResponse(r, err, nil, requestId)
		return
	}
	SendResponse(r, nil, "ok", requestId)
}
