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
from django.utils.translation import ugettext_lazy as _

from ..base import DataAPI
from ..domains import BACKUP_APIGW_DOMAIN


class _BackupApi(object):
    MODULE = _("备份文件下载")

    def __init__(self):
        self.query = DataAPI(
            method="POST",
            base=BACKUP_APIGW_DOMAIN,
            url="backupapi/query",
            module=self.MODULE,
            description=_("获取备份"),
        )

        self.download = DataAPI(
            method="POST",
            base=BACKUP_APIGW_DOMAIN,
            url="backupapi/recover",
            module=self.MODULE,
            description=_("备份文件下载"),
        )

        self.download_result = DataAPI(
            method="GET",
            base=BACKUP_APIGW_DOMAIN,
            url="backupapi/get_recover_result",
            module=self.MODULE,
            description=_("查询单据状态"),
        )
        self.download_backup_client = DataAPI(
            method="POST",
            base=BACKUP_APIGW_DOMAIN,
            url="backupapi/client/install",
            module=self.MODULE,
            description=_("backup_client下载，同步任务"),
            default_timeout=300,
        )


MysqlBackupApi = _BackupApi()
RedisBackupApi = _BackupApi()
