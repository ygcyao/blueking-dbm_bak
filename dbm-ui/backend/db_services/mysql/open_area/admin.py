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
from django.contrib import admin

from . import models


@admin.register(models.TendbOpenAreaConfig)
class TendbOpenAreaConfigAdmin(admin.ModelAdmin):
    list_display = ("bk_biz_id", "config_name", "updater", "cluster_type")
    list_filter = ("bk_biz_id", "config_name", "cluster_type")
    search_fields = ("bk_biz_id", "config_name")
