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


@admin.register(models.DBAdministrator)
class DBAAdmin(admin.ModelAdmin):
    list_display = ("bk_biz_id", "db_type", "users")
    list_filter = ("db_type",)
    search_fields = ("users",)


@admin.register(models.SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ("type", "key", "value", "desc")
    search_fields = (
        "type",
        "key",
    )


@admin.register(models.BizSettings)
class BizSettingsAdmin(admin.ModelAdmin):
    list_display = ("bk_biz_id", "type", "key", "value", "desc")
    search_fields = (
        "type",
        "key",
    )


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "label", "values")
    list_filter = ("label",)
    search_fields = ("username",)


@admin.register(models.PasswordPolicy)
class PasswordPolicyAdmin(admin.ModelAdmin):
    list_display = ("account_type", "policy")
    search_fields = ("account_type",)


@admin.register(models.FunctionController)
class FunctionControllerAdmin(admin.ModelAdmin):
    list_display = ("name", "is_enabled", "is_frozen", "parent_name")
    list_filter = ("is_enabled", "is_frozen")
    search_fields = ("name",)
