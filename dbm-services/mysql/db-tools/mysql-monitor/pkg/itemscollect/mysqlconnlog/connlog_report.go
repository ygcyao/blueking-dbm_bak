// TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
// Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
// Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
// You may obtain a copy of the License at https://opensource.org/licenses/MIT
// Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
// an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
// specific language governing permissions and limitations under the License.

package mysqlconnlog

import (
	"time"
)

type connRecord struct {
	ConnId       int64     `db:"conn_id" json:"conn_id"`
	ConnTime     time.Time `db:"conn_time" json:"conn_time"`
	UserName     string    `db:"user_name" json:"user_name"`
	CurUserName  string    `db:"cur_user_name" json:"cur_user_name"`
	Ip           string    `db:"ip" json:"ip"`
	BkBizId      int       `json:"bk_biz_id"`
	BkCloudId    *int      `json:"bk_cloud_id"`
	ImmuteDomain string    `json:"immute_domain"`
	Port         int       `json:"port"`
	MachineType  string    `json:"machine_type"`
	Role         *string   `json:"role"`
}

//func mysqlConnLogReport(db *sqlx.DB) (string, error) {
//	ctx, cancel := context.WithTimeout(context.Background(), config.MonitorConfig.InteractTimeout)
//	defer cancel()
//
//	conn, err := db.Connx(ctx)
//	if err != nil {
//		slog.Error("connlog report get conn from db", slog.String("error", err.Error()))
//		return "", err
//	}
//	defer func() {
//		_ = conn.Close()
//	}()
//
//	var _r interface{}
//	err = conn.GetContext(ctx, &_r,
//		`SELECT 1 FROM INFORMATION_SCHEMA.TABLES
//					WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ? AND TABLE_TYPE='BASE TABLE'`,
//		cst.DBASchema, "conn_log_old")
//	if err != nil {
//		if errors.Is(err, sql.ErrNoRows) {
//			slog.Info("conn_log_old not found, skip report")
//			return "", nil
//		} else {
//			slog.Error("check conn_log_old exists", slog.String("error", err.Error()))
//			return "", err
//		}
//	}
//
//	// report 会把 old 表删掉, 所以也要禁用 binlog 防止从 master 到 slave
//	_, err = conn.ExecContext(ctx, `SET SQL_LOG_BIN=0`)
//	if err != nil {
//		slog.Error("disable binlog", slog.String("error", err.Error()))
//		return "", err
//	}
//	slog.Info("report conn log disable binlog success")
//
//	reportFilePath := filepath.Join(cst.DBAReportBase, "mysql", "conn_log", "report.log")
//	err = os.MkdirAll(filepath.Dir(reportFilePath), 0755)
//	if err != nil {
//		slog.Error("make report dir", slog.String("error", err.Error()))
//		return "", err
//	}
//	slog.Info("make report dir", slog.String("dir", filepath.Dir(reportFilePath)))
//
//	f, err := os.OpenFile(
//		reportFilePath,
//		os.O_CREATE|os.O_TRUNC|os.O_RDWR,
//		0755,
//	)
//	if err != nil {
//		slog.Error("open conn log report file", slog.String("error", err.Error()))
//		return "", err
//	}
//	slog.Info("open conn report file", slog.String("file path", f.Name()))
//
//	lf := ratelimit.Writer(f, ratelimit.NewBucketWithRate(float64(speedLimit), speedLimit))
//
//	rows, err := conn.QueryxContext(ctx, fmt.Sprintf(`SELECT * FROM %s.conn_log_old`, cst.DBASchema))
//	if err != nil {
//		slog.Error("connlog report query conn_log_old", slog.String("error", err.Error()))
//		return "", err
//	}
//	defer func() {
//		_ = rows.Close()
//	}()
//
//	for rows.Next() {
//		cr := connRecord{
//			BkBizId:      config.MonitorConfig.BkBizId,
//			BkCloudId:    config.MonitorConfig.BkCloudID,
//			ImmuteDomain: config.MonitorConfig.ImmuteDomain,
//			// Ip:           config.MonitorConfig.Ip,
//			Port:        config.MonitorConfig.Port,
//			MachineType: config.MonitorConfig.MachineType,
//			Role:        config.MonitorConfig.Role,
//		}
//		err := rows.StructScan(&cr)
//		if err != nil {
//			slog.Error("scan conn_log record", slog.String("error", err.Error()))
//			return "", err
//		}
//
//		content, err := json.Marshal(cr)
//		if err != nil {
//			slog.Error("marshal conn record", slog.String("error", err.Error()))
//			return "", err
//		}
//
//		_, err = lf.Write(append(content, []byte("\n")...))
//		if err != nil {
//			slog.Error("write conn report", slog.String("error", err.Error()))
//			return "", err
//		}
//	}
//
//	_, err = db.ExecContext(ctx, fmt.Sprintf(`DROP TABLE IF EXISTS %s.conn_log_old`, cst.DBASchema))
//	if err != nil {
//		slog.Error("drop conn_log_old", slog.String("error", err.Error()))
//		return "", err
//	}
//	slog.Info("drop conn_log_old")
//
//	return "", nil
//}
