import http from './http';
import type { ListBase } from './types/common';

interface IResult {
  results: Record<string, unknown>[],
  name: string,
  title: {
    name: string,
    display_name: string,
    format: 'text'|'status'|'fail_slave_instance'
  }[]
}
// 数据校验
export const getChecksumReport = function (params: Record<string, any>) {
  return http.get<IResult>('/db_report/checksum_check/report', params);
};

// 失败的从库实例详情
export const getChecksumInstance = function (params: Record<string, any>) {
  return http.get<ListBase<{
    details: Record<string, string[]>,
    id: number,
    ip: string,
    master_ip: string,
    master_port: string,
    port: string
  }[]>>('/db_report/checksum_check/instance', params);
};


// 元数据检查报告列表
export const getMetaCheckInsganceBelong = function (params: Record<string, any>) {
  return http.get<IResult>('/db_report/meta_check/instance_belong', params);
};

// binlog检查报告
export const getmysqlCheckBinlogBackup = function (params: Record<string, any>) {
  return http.get<IResult>('/db_report/mysql_check/binlog_backup', params);
};

// 全备检查报告
export const getmysqlCheckFullBackup = function (params: Record<string, any>) {
  return http.get<IResult>('/db_report/mysql_check/full_backup', params);
};
