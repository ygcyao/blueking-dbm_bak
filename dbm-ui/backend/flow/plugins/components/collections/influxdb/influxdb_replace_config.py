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
import logging
from typing import List

from pipeline.component_framework.component import Component
from pipeline.core.flow.activity import Service

from backend.components import DBConfigApi
from backend.components.dbconfig.constants import ConfType, FormatType, LevelName, OpType, ReqType
from backend.db_meta.api import common
from backend.db_meta.enums import InstanceRole
from backend.db_meta.models import StorageInstance
from backend.flow.consts import ConfigTypeEnum, LevelInfoEnum, NameSpaceEnum
from backend.flow.plugins.components.collections.common.base_service import BaseService

logger = logging.getLogger("flow")


class InfluxdbReplaceConfigService(BaseService):
    """
    更新config
    """

    def _execute(self, data, parent_data) -> bool:
        global_data = data.get_one_of_inputs("global_data")

        for influxdb in global_data["new_nodes"]["influxdb"]:
            data = DBConfigApi.query_conf_item(
                {
                    "bk_biz_id": str(global_data["bk_biz_id"]),
                    "level_name": LevelName.INSTANCE,
                    "level_value": str(influxdb["instance_id"]),
                    "level_info": {"module": LevelInfoEnum.TendataModuleDefault, "cluster": "0"},
                    "conf_file": influxdb["db_version"],
                    "conf_type": ConfType.DBCONF,
                    "namespace": NameSpaceEnum.Influxdb,
                    "format": FormatType.MAP,
                }
            )
            config = data["content"]

            config_map = {
                "username": config["username"],
                "password": config["password"],
            }

            conf_items = []
            for conf_name, conf_value in config_map.items():
                conf_items.append({"conf_name": conf_name, "conf_value": conf_value, "op_type": OpType.UPDATE})

            storage_instances = []
            storage_instances.append(
                {
                    "ip": influxdb["ip"],
                    "port": influxdb["port"],
                    "instance_role": InstanceRole.INFLUXDB.value,
                }
            )
            storage_objs = common.filter_out_instance_obj(storage_instances, StorageInstance.objects.all())
            for storage_obj in storage_objs:
                DBConfigApi.upsert_conf_item(
                    {
                        "conf_file_info": {
                            "conf_file": influxdb["db_version"],
                            "conf_type": ConfigTypeEnum.DBConf,
                            "namespace": NameSpaceEnum.Influxdb,
                        },
                        "level_info": {"module": LevelInfoEnum.TendataModuleDefault, "cluster": "0"},
                        "conf_items": conf_items,
                        "bk_biz_id": str(global_data["bk_biz_id"]),
                        "level_name": LevelName.INSTANCE,
                        "level_value": str(storage_obj.id),
                        "confirm": 0,
                        "req_type": ReqType.SAVE_AND_PUBLISH,
                    }
                )

        self.log_info("DBConfig re successfully")
        return True

    def inputs_format(self) -> List:
        return [
            Service.InputItem(name="kwargs", key="kwargs", type="dict", required=True),
            Service.InputItem(name="global_data", key="global_data", type="dict", required=True),
        ]

    def outputs_format(self) -> List:
        return [Service.OutputItem(name="command result", key="result", type="str")]


class InfluxdbReplaceConfigComponent(Component):
    name = __name__
    code = "influxdb_replace_config"
    bound_service = InfluxdbReplaceConfigService
