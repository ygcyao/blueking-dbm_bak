/*
 * TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
 *
 * Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
 *
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at https://opensource.org/licenses/MIT
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
 * the specific language governing permissions and limitations under the License.
*/

import type { TicketTypesStrings } from '@common/const';

import http from '../http';
import type { ListBase } from '../types';

const path = '/apis/taskflow';

/**
 * 任务流程节点类型
 * ServiceActivity 服务节点（可点击查看）
 * ConvergeGateway 汇聚网关
 * ParallelGateway 并行网关
 * SubProcess 子流程
 * EmptyStartEvent 开始节点
 * EmptyEndEvent 结束节点
 */
export enum FlowTypes {
  ServiceActivity = 'ServiceActivity',
  SubProcess = 'SubProcess',
  ConvergeGateway = 'ConvergeGateway',
  ParallelGateway = 'ParallelGateway',
  EmptyStartEvent = 'EmptyStartEvent',
  EmptyEndEvent = 'EmptyEndEvent',
}

/**
 * 查询任务列表参数
 */
interface GetTaskflowParams {
  bk_biz_id: number,
  limit: number,
  offset: number
  root_id?: string,
  uid?: number,
  status?: string,
  status__in?: string,
  ticket_type?: string,
  ticket_type__in?: string,
  created_at__gte?: string,
  created_at__lte?: string,
}

/**
 * 任务列表项
 */
interface TaskflowItem {
  root_id: string,
  ticket_type_display: string,
  ticket_type: TicketTypesStrings,
  status: string,
  uid: string,
  created_by: string,
  created_at: string,
  cost_time: number,
  bk_biz_id: number,
  bk_host_ids?: number[],
}

/**
 * 查询任务列表
 */
export function getTaskflow(params: GetTaskflowParams) {
  return http.get<ListBase<TaskflowItem[]>>(`${path}/`, params);
}

/**
 * 指定目录下载（返回下载链接）
 */
export function getRedisFileUrls(params: {
  root_id: string,
  paths: string[]
}) {
  return http.post<Record<string, string>>(`${path}/redis/download_dirs/`, params);
}

/**
 * 结果文件列表信息
 */
interface KeyFileItem {
  name: string,
  size: number,
  size_display: string,
  domain: string,
  created_time: string,
  cluster_alias: string,
  path: string,
  cluster_id: number,
  files: {
    size: string,
    name: string,
    md5: string,
    full_path: string,
    created_time: string,
  }[]
}

/**
 * 结果文件列表
 */
export function getKeyFiles(params: { rootId: string }) {
  return http.get<KeyFileItem[]>(`${path}/redis/${params.rootId}/key_files/`);
}

/**
 * 任务流程节点数据
 */
interface FlowItem {
  id: string,
  name: string | null,
  incoming: string | string[],
  outgoing: string | string[],
  type: keyof typeof FlowTypes,
  error_ignorable?: boolean,
  optional?: boolean,
  retryable?: boolean,
  skippable?: boolean,
  status?: 'FINISHED' | 'RUNNING' | 'FAILED' | 'READY' | 'CREATED' | 'SKIPPED',
  timeout?: number,
  started_at?: number,
  created_at?: number,
  updated_at?: number,
  component?: {
    code: string
  },
  pipeline?: FlowsData,
}

/**
 * 任务流程数据
 */
interface FlowsData {
  id: string,
  data: any,
  end_event: FlowItem,
  start_event: FlowItem,
  flows: {
    [key: string]: {
      id: string,
      source: string,
      target: string,
      is_default: boolean
    }
  },
  gateways: { [key: string]: FlowItem },
  activities: { [key: string]: FlowItem },
  flow_info: TaskflowItem,
}

/**
 * 任务详情
 */
export function getTaskflowDetails(params: { rootId: string }) {
  return http.get<FlowsData>(`${path}/${params.rootId}/`);
}

/**
 * 节点版本列表
 */
export function getRetryNodeHistories(params: {
  root_id: string,
  node_id: string
}) {
  return http.get<{
    started_time: string,
    version: string,
    cost_time: number
  }[]>(`${path}/${params.root_id}/node_histories/`, params);
}

/**
 * 节点日志
 */
export function getNodeLog(params: {
  root_id: string,
  node_id: string,
  version_id: string
}) {
  return http.get<{
    timestamp: number,
    message: string,
    levelname: string,
  }[]>(`${path}/${params.root_id}/node_log/`, params);
}

/**
 * 重试节点
 */
export function retryTaskflowNode(params: {
  root_id: string,
  node_id: string
}) {
  return http.post<{ node_id: string }>(`${path}/${params.root_id}/retry_node/`, params);
}

/**
 * 撤销流程
 */
export function revokePipeline(params: { rootId: string }) {
  return http.post(`${path}/${params.rootId}/revoke_pipeline/`);
}

/**
 * 跳过节点
 */
export function skipTaskflowNode(params: {
  root_id: string,
  node_id: string
}) {
  return http.post<{ node_id: string }>(`${path}/${params.root_id}/skip_node/`, params);
}

/**
 * 强制失败节点
 */
export function forceFailflowNode(params: {
  root_id: string,
  node_id: string
}) {
  return http.post<{ node_id: string }>(`${path}/${params.root_id}/force_fail_node/`, params);
}
