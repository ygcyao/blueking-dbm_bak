# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from blue_krill.data_types.enum import StructuredEnum


class DestroyedStatus(int, StructuredEnum):
    """
    销毁状态枚举
    """

    NOT_DESTROYED = 0  # 未销毁
    DESTROYING = 1  # 销毁中
    DESTROYED = 2  # 已销毁


class MigrateStatus(int, StructuredEnum):
    """
    slots 迁移状态枚举
    """

    NOT_STARTED = 0  # 未开始
    EXECUTING = 1  # 执行中
    COMPLETED = 2  # 已完成
    ERROR_OCCURRED = -1  # 错误


class DataStructureStatus(int, StructuredEnum):
    """
    数据构造状态枚举
    """

    NOT_STARTED = 0  # 未开始
    EXECUTING = 1  # 执行中
    COMPLETED = 2  # 已完成
    ERROR_OCCURRED = -1  # 错误
