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
from rest_framework.decorators import action
from rest_framework.response import Response

from backend.bk_web.viewsets import SystemViewSet
from backend.iam_app.handlers.drf_perm import DBManageIAMPermission

from . import serializers
from .pagination import ResourceLimitOffsetPagination
from .query import ListRetrieveResource


class ResourceViewSet(SystemViewSet):
    """资源查询基类"""

    lookup_field = "cluster_id"

    query_class = ListRetrieveResource
    query_serializer_class = None
    list_instances_slz = serializers.ListInstancesSerializer
    retrieve_instances_slz = serializers.RetrieveInstancesSerializer

    pagination_class = ResourceLimitOffsetPagination

    def _get_custom_permissions(self):
        return [DBManageIAMPermission()]

    def retrieve(self, request, bk_biz_id: int, cluster_id: int):
        """查询集群详情"""
        return Response(self.query_class.retrieve_cluster(bk_biz_id, cluster_id))

    def list(self, request, bk_biz_id: int):
        """查询集群列表"""
        query_params = self.params_validate(self.query_serializer_class)
        data = self.paginator.paginate_list(request, bk_biz_id, self.query_class.list_clusters, query_params)
        return self.get_paginated_response(data)

    @action(methods=["GET"], detail=False, url_path="list_instances")
    def list_instances(self, request, bk_biz_id: int):
        """查询实例列表"""
        query_params = self.params_validate(self.list_instances_slz)
        data = self.paginator.paginate_list(request, bk_biz_id, self.query_class.list_instances, query_params)
        return self.get_paginated_response(data)

    @action(methods=["GET"], detail=False, url_path="retrieve_instance")
    def retrieve_instance(self, request, bk_biz_id: int):
        """查询实例详情"""
        query_params = self.params_validate(self.retrieve_instances_slz)
        return Response(
            self.query_class.retrieve_instance(
                bk_biz_id, query_params.get("cluster_id"), query_params["ip"], query_params["port"]
            )
        )

    @action(methods=["GET"], detail=False, url_path="get_table_fields")
    def get_table_fields(self, request, bk_biz_id):
        """获取 table 信息"""
        return Response(self.query_class.get_fields())

    @action(methods=["GET"], detail=True, url_path="get_topo_graph")
    def get_topo_graph(self, request, bk_biz_id: int, cluster_id: int):
        """获取拓扑图"""
        return Response(self.query_class.get_topo_graph(bk_biz_id, cluster_id))

    @action(methods=["POST", "GET"], detail=False, url_path="export_cluster")
    def export_cluster(self, request, bk_biz_id: int):
        """导出集群数据为 excel 文件"""
        cluster_ids = request.POST.get("cluster_ids")
        return self.query_class.export_cluster(bk_biz_id, cluster_ids)

    @action(methods=["POST", "GET"], detail=False, url_path="export_instance")
    def export_instance(self, request, bk_biz_id: int):
        """导出实例数据为 excel 文件"""
        bk_host_ids = request.POST.get("bk_host_ids")
        return self.query_class.export_instance(bk_biz_id, bk_host_ids)

    def _paginate_resource_list(self, request, bk_biz_id: int):
        return self.paginator.paginate_resource_list(request, bk_biz_id, self)
