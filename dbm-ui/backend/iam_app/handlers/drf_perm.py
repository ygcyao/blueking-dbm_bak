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
import binascii
import logging
from typing import List

from bk_audit.constants.log import DEFAULT_EMPTY_VALUE, DEFAULT_SENSITIVITY
from bk_audit.contrib.bk_audit.client import bk_audit_client
from bk_audit.log.exporters import BaseExporter
from bk_audit.log.models import AuditContext, AuditInstance
from django.utils.translation import ugettext as _
from iam import Resource
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from backend import env
from backend.core.encrypt.constants import AsymmetricCipherConfigType
from backend.core.encrypt.exceptions import RSADecryptException
from backend.core.encrypt.handlers import AsymmetricHandler
from backend.db_proxy.constants import DB_CLOUD_TOKEN_EXPIRE_TIME
from backend.flow.models import FlowTree
from backend.iam_app.dataclass.actions import ActionEnum, ActionMeta
from backend.iam_app.dataclass.resources import BusinessResourceMeta
from backend.iam_app.handlers.permission import Permission
from backend.ticket.models import Ticket
from backend.utils.redis import RedisConn

logger = logging.getLogger("root")


class CommonInstance(object):
    def __init__(self, data):
        self.instance_id = data.get("id", DEFAULT_EMPTY_VALUE)
        self.instance_name = data.get("name", DEFAULT_EMPTY_VALUE)
        self.instance_sensitivity = data.get("sensitivity", DEFAULT_SENSITIVITY)
        self.instance_origin_data = data.get("origin_data", DEFAULT_EMPTY_VALUE)
        self.instance_data = data

    @property
    def instance(self):
        return AuditInstance(self)


class ConsoleExporter(BaseExporter):
    is_delay = False

    def export(self, events):
        for event in events:
            print(event.to_json_str())


bk_audit_client.add_exporter(ConsoleExporter())


class IAMPermission(permissions.BasePermission):
    """
    作为drf-iam鉴权的基类
    """

    resource_type = None

    def __init__(self, actions: List[ActionMeta], resources: List[Resource] = None) -> None:
        self.actions = actions
        self.resources = resources or []

    def has_permission(self, request, view):
        iam = Permission(request=request)
        context = AuditContext(request=request)
        # 查询类请求（简单定义为所有 GET 请求）不审计
        if request.method != "GET":
            # 审计操作类请求
            for action in self.actions:
                if not self.resources:
                    bk_audit_client.add_event(action=action, audit_context=context)
                for resource in self.resources:
                    bk_audit_client.add_event(
                        action=action,
                        resource_type=self.resource_type() if self.resource_type else resource,
                        audit_context=context,
                        instance=CommonInstance(resource.attribute),
                    )

        # 如果是超级用户或忽略鉴权，则跳过鉴权
        if request.user.is_superuser or env.BK_IAM_SKIP:
            return True

        # 如果没有动作请求，则跳过鉴权
        if not self.actions:
            return True

        for action in self.actions:
            iam.is_allowed(action=action, resources=self.resources, is_raise_exception=True)

        return True

    def has_object_permission(self, request, view, obj):
        """
        这个方法由子类各自去实现, 通常是子类构造出resource
        """

        return self.has_permission(request, view)


class BusinessIAMPermission(IAMPermission):
    """
    业务相关动作的鉴权
    """

    resource_type = BusinessResourceMeta

    def __init__(self, actions: List[ActionMeta], resources: List[Resource] = None, bk_biz_id: int = None) -> None:
        self.bk_biz_id = bk_biz_id
        super().__init__(actions, resources)

    def _fetch_biz_id(self, request, view):
        # 从view.kwargs, request.data, request.query_params中尝试获取业务id
        bk_biz_id = self.bk_biz_id or view.kwargs.get("bk_biz_id", 0)
        if not bk_biz_id:
            bk_biz_id = request.data.get("bk_biz_id", 0) or request.query_params.get("bk_biz_id", 0)

        return bk_biz_id

    def has_permission(self, request, view):
        bk_biz_id = self._fetch_biz_id(request, view)
        if not int(bk_biz_id):
            return True

        self.resources = [BusinessResourceMeta.create_instance(str(bk_biz_id))]
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        # 判断当前对象obj是否有bk_biz_id
        obj_bk_biz_id = obj.bk_biz_id if hasattr(obj, "bk_biz_id") else 0
        bk_biz_id = self.bk_biz_id or obj_bk_biz_id
        if bk_biz_id:
            self.resources = [BusinessResourceMeta.create_instance(str(bk_biz_id))]
            return super().has_object_permission(request, view, obj)

        # 否则从view/POST/GET中获取bk_biz_id
        return self.has_permission(request, view)


class RejectPermission(permissions.BasePermission):
    """
    永假的权限，用于屏蔽那些拒绝访问的接口
    """

    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class ViewBusinessIAMPermission(BusinessIAMPermission):
    """
    业务查看——鉴权
    """

    def __init__(self, bk_biz_id: int = None):
        super().__init__([ActionEnum.VIEW_BUSINESS], bk_biz_id=bk_biz_id)


class DBManageIAMPermission(BusinessIAMPermission):
    """
    数据库管理Permission类
    """

    def __init__(self, bk_biz_id: int = None):
        super().__init__([ActionEnum.DB_MANAGE], bk_biz_id=bk_biz_id)

    def _fetch_key_id(self, request, view, key):
        key_id = view.kwargs.get(key) or request.data.get(key) or request.query_params.get(key)
        return key_id


class GlobalManageIAMPermission(IAMPermission):
    """
    平台管理Permission类
    """

    def __init__(self):
        super().__init__([ActionEnum.GLOBAL_MANAGE])


class TaskFlowIAMPermission(DBManageIAMPermission):
    def _fetch_biz_id(self, request, view):
        bk_biz_id = super()._fetch_biz_id(request, view)
        if not bk_biz_id:
            root_id = self._fetch_key_id(request, view, key="root_id")
            if root_id:
                bk_biz_id = FlowTree.objects.get(root_id=root_id).bk_biz_id

        return bk_biz_id


class TicketIAMPermission(DBManageIAMPermission):
    def _fetch_biz_id(self, request, view):
        bk_biz_id = super()._fetch_biz_id(request, view)
        if not bk_biz_id:
            ticket_id = self._fetch_key_id(request, view, key="id")
            if ticket_id:
                bk_biz_id = Ticket.objects.get(id=ticket_id).bk_biz_id

        return bk_biz_id


class DBEventIAMPermission(DBManageIAMPermission):
    # TODO: 切换事件的临时鉴权类，后续再新版权限会删除
    def _fetch_biz_id(self, request, view):
        bk_biz_id = self._fetch_key_id(request, view, key="app")
        return bk_biz_id


class IsAuthenticatedPermission(permissions.BasePermission):
    """
    用户认证
    """

    def has_authenticated_permission(self, request, view):
        return permissions.IsAuthenticated().has_permission(request, view)

    def has_permission(self, request, view):
        return permissions.IsAuthenticated().has_permission(request, view)


class ProxyPassPermission(permissions.BasePermission):
    """
    透传接口权限
    """

    @classmethod
    def verify_token(cls, db_cloud_token, bk_cloud_id):
        try:
            token = AsymmetricHandler.decrypt(name=AsymmetricCipherConfigType.PROXYPASS.value, content=db_cloud_token)
        except (RSADecryptException, binascii.Error, KeyError, IndexError):
            raise PermissionDenied(_("db_cloud_token:{}解密失败，请检查token是否合法").format(db_cloud_token))

        token_cloud_id = int(token.split("_")[0])
        if token_cloud_id != int(bk_cloud_id):
            raise PermissionDenied(
                _("解析的云区域(ID:{})与请求参数的云区域(ID:{})不相同，请检查token是否合法").format(token_cloud_id, bk_cloud_id)
            )

    def has_permission(self, request, view):

        # 如果是直连区域的内部调用，不进行token校验
        if getattr(request, "internal_call", None):
            return True

        db_cloud_token = request.data.get("db_cloud_token", "")
        bk_cloud_id = request.data.get("bk_cloud_id")
        cache_key = f"cache_db_cloud_token_{bk_cloud_id}"
        # 判断是否在缓存集合中，不在cache中则走解密流程并cache。
        # 由于Redis的list不能直接判断元素是否存在，所以选择set存取
        if not RedisConn.sismember(cache_key, db_cloud_token):
            self.verify_token(db_cloud_token, bk_cloud_id)
            # 如果这个cache_key刚创建，则需要设置过期时间
            if not RedisConn.exists(cache_key):
                RedisConn.sadd(cache_key, db_cloud_token)
                RedisConn.expire(cache_key, DB_CLOUD_TOKEN_EXPIRE_TIME)
            else:
                RedisConn.sadd(cache_key, db_cloud_token)
        request.data.pop("db_cloud_token")
        return True
