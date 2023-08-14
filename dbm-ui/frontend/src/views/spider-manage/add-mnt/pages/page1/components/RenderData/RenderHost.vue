<!--
 * TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-DB管理系统(BlueKing-BK-DBM) available.
 *
 * Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
 *
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License athttps://opensource.org/licenses/MIT
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for
 * the specific language governing permissions and limitations under the License.
-->

<template>
  <div class="render-host-box">
    <TableEditInput
      ref="inputRef"
      class="host-input"
      :disabled="!clusterData"
      :model-value="localHostList.map(item => item.ip).join(',')"
      :placeholder="t('请输入单个IP')"
      readonly
      :rules="rules"
      textarea />
    <div
      v-if="Boolean(clusterData)"
      class="edit-btn"
      @click="handleShowIpSelector">
      <DbIcon type="host-select" />
    </div>
  </div>
  <IpSelector
    v-if="clusterData"
    v-model:show-dialog="isShowIpSelector"
    :biz-id="clusterData.bk_biz_id"
    button-text=""
    :cloud-info="{
      id: clusterData.bk_cloud_id,
      name: clusterData.bk_cloud_name
    }"
    :data="localHostList"
    service-mode="all"
    :show-view="false"
    @change="handleHostChange" />
</template>
<script setup lang="ts">
  import {
    ref,
    shallowRef,
  } from 'vue';
  import { useI18n } from 'vue-i18n';

  import type SpiderModel from '@services/model/spider/spider';
  import type { HostDetails } from '@services/types/ip';

  import IpSelector from '@components/ip-selector/IpSelector.vue';

  import TableEditInput from '@views/mysql/common/edit/Input.vue';

  interface Props {
    clusterData?: SpiderModel
  }

  interface Exposes {
    getValue: () => Promise<Array<string>>
  }

  defineProps<Props>();

  const { t } = useI18n();
  const inputRef = ref();
  const isShowIpSelector = ref(false);

  const localHostList = shallowRef<HostDetails[]>([]);

  const rules = [
    {
      validator: (value: string) => Boolean(value),
      message: t('运维节点 IP 不能为空'),
    },
  ];

  const handleShowIpSelector = () => {
    isShowIpSelector.value = true;
  };

  const handleHostChange = (hostList: HostDetails[]) => {
    localHostList.value = hostList;
  };

  defineExpose<Exposes>({
    getValue() {
      const formatHost = (hostList: HostDetails[]) => hostList.map(item => ({
        bk_host_id: item.host_id,
        ip: item.ip,
        bk_cloud_id: item.cloud_area.id,
      }));

      return inputRef.value
        .getValue()
        .then(() => Promise.resolve({
          spider_ip_list: formatHost(localHostList.value),
        }));
    },
  });
</script>
<style lang="less" scoped>
  .render-host-box {
    position: relative;
    display: flex;
    align-items: center;

    .host-input{
      flex: 1;
    }

    .edit-btn{
      display: flex;
      width: 24px;
      height: 24px;
      cursor: pointer;
      background: #F0F1F5;
      border-radius: 2px;
      align-items: center;
      justify-content: center;
    }
  }
</style>