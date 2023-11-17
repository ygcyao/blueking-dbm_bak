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
import logging.config
from dataclasses import asdict
from typing import Dict, Optional

from django.utils.translation import ugettext as _

from backend.configuration.constants import DBType
from backend.flow.consts import DBA_ROOT_USER
from backend.flow.engine.bamboo.scene.common.builder import Builder, SubBuilder
from backend.flow.engine.bamboo.scene.common.get_file_list import GetFileList
from backend.flow.plugins.components.collections.riak.exec_actuator_script import ExecuteRiakActuatorScriptComponent
from backend.flow.plugins.components.collections.riak.get_riak_cluster_node import GetRiakClusterNodeComponent
from backend.flow.plugins.components.collections.riak.riak_db_meta import RiakDBMetaComponent
from backend.flow.plugins.components.collections.riak.trans_files import TransFileComponent
from backend.flow.utils.riak.riak_act_dataclass import (
    DBMetaFuncKwargs,
    DownloadMediaKwargs,
    DownloadMediaKwargsFromTrans,
)
from backend.flow.utils.riak.riak_act_payload import RiakActPayload
from backend.flow.utils.riak.riak_context_dataclass import NodesContext, RiakActKwargs
from backend.flow.utils.riak.riak_db_meta import RiakDBMeta

logger = logging.getLogger("flow")


class RiakRebootFlow(object):
    """
    Riak集群启用的抽象类
    {
    "uid": "2022111212001000",
    "root_id": 123,
    "created_by": "admin",
    "bk_biz_id": 0,
    "ticket_type": "RIAK_REBOOT",
    "bk_cloud_id": 0,
    "ip": "0.0.0.0"
    }
    """

    def __init__(self, root_id: str, data: Optional[Dict]):
        """
        @param root_id : 任务流程定义的root_id
        @param data : 单据传递过来的参数列表，是dict格式
        """
        self.root_id = root_id
        self.data = data

    def riak_reboot_flow(self):
        """
        Riak实例重启
        """
        riak_pipeline = Builder(root_id=self.root_id, data=self.data)
        sub_pipeline = SubBuilder(root_id=self.root_id, data=self.data)

        sub_pipeline.add_act(
            act_name=_("下发actuator以及riak介质"),
            act_component_code=TransFileComponent.code,
            kwargs=asdict(
                DownloadMediaKwargs(
                    exec_ip=self.data["ip"],
                    bk_cloud_id=self.data["bk_cloud_id"],
                    file_list=GetFileList(db_type=DBType.Riak).get_db_actuator_package(),
                )
            ),
        )

        sub_pipeline.add_act(
            act_name=_("actuator_重启riak实例"),
            act_component_code=ExecuteRiakActuatorScriptComponent.code,
            kwargs=asdict(
                RiakActKwargs(
                    exec_ip=self.data["ip"],
                    bk_cloud_id=self.data["bk_cloud_id"],
                    run_as_system_user=DBA_ROOT_USER,
                    get_riak_payload_func=RiakActPayload.get_restart_payload.__name__,
                )
            ),
        )

        riak_pipeline.add_sub_pipeline(sub_pipeline.build_sub_process(sub_name=_("Riak重启实例")))
        riak_pipeline.run_pipeline(init_trans_data_class=NodesContext())