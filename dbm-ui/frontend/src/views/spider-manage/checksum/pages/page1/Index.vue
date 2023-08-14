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
  <SmartAction>
    <div class="spider-manage-checksum-page">
      <BkAlert
        closable
        theme="info"
        :title="t('数据校验修复：对集群的主库和从库进行数据一致性校验和修复，其中 MyISAM  引擎库表不会被校验和修复')" />
      <RenderData
        class="mt16"
        @batch-select-cluster="handleShowBatchSelector">
        <RenderDataRow
          v-for="(item, index) in tableData"
          :key="item.rowKey"
          ref="rowRefs"
          :data="item"
          :removeable="tableData.length < 2"
          @add="(payload: Array<IDataRow>) => handleAppend(index, payload)"
          @remove="handleRemove(index)" />
      </RenderData>
      <BkForm
        class="mt-24 form-block"
        form-type="vertical"
        :model="formData">
        <BkFormItem
          :label="t('指定执行时间')"
          property="timing"
          required>
          <BkDatePicker
            v-model="formData.timing"
            style="width: 360px"
            type="datetime" />
        </BkFormItem>
        <BkFormItem
          :label="t('全局超时时间（h）')"
          property="runtime_hour"
          required>
          <BkInput
            v-model="formData.runtime_hour"
            :max="168"
            :min="24"
            style="width: 360px"
            type="number" />
        </BkFormItem>
        <BkFormItem
          :label="t('修复数据')"
          property="data_repair.is_repair"
          required>
          <BkSwitcher
            v-model="formData.data_repair.is_repair"
            theme="primary" />
        </BkFormItem>
        <BkFormItem
          v-if="formData.data_repair.is_repair"
          :label="t('修复模式')"
          property="data_repair.mode">
          <BkRadioGroup
            v-model="formData.data_repair.mode"
            class="repair-mode-block">
            <div class="item-box">
              <BkRadio label="manual">
                <div class="item-content">
                  <DbIcon
                    class="item-flag"
                    type="account" />
                  <div class="item-label">
                    {{ $t('手动执行') }}
                  </div>
                  <div>{{ $t('单据审批通过之后_需要人工确认方可执行') }}</div>
                </div>
              </BkRadio>
            </div>
            <div class="item-box">
              <BkRadio label="timer">
                <div class="item-content">
                  <DbIcon
                    class="item-flag"
                    type="timed-task" />
                  <div class="item-label">
                    {{ $t('定时执行') }}
                  </div>
                  <div>{{ $t('单据审批通过之后_定时执行_无需确认') }}</div>
                </div>
              </BkRadio>
            </div>
          </BkRadioGroup>
        </BkFormItem>
      </BkForm>
      <ClusterSelector
        v-model:is-show="isShowBatchSelector"
        :get-resource-list="getList"
        :selected="{}"
        :tab-list="clusterSelectorTabList"
        @change="handelClusterChange" />
    </div>
    <template #action>
      <BkButton
        class="w-88"
        :loading="isSubmitting"
        theme="primary"
        @click="handleSubmit">
        {{ t('提交') }}
      </BkButton>
      <DbPopconfirm
        :confirm-handler="handleReset"
        :content="t('重置将会情况当前填写的所有内容_请谨慎操作')"
        :title="t('确认重置页面')">
        <BkButton
          class="ml8 w-88"
          :disabled="isSubmitting">
          {{ t('重置') }}
        </BkButton>
      </DbPopconfirm>
    </template>
  </SmartAction>
</template>
<script setup lang="tsx">
  import dayjs from 'dayjs';
  import {
    reactive,
    ref,
    shallowRef,
  } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { useRouter } from 'vue-router';

  import { getList } from '@services/spider';
  import { createTicket } from '@services/ticket';

  import { useGlobalBizs } from '@stores';

  import { ClusterTypes } from '@common/const';

  import ClusterSelector from '@components/cluster-selector/SpiderClusterSelector.vue';

  import RenderData from './components/RenderData/Index.vue';
  import RenderDataRow, {
    createRowData,
    type IDataRow,
  } from './components/RenderData/Row.vue';

  interface IClusterData {
    id: number,
    master_domain: string
  }

  // 检测列表是否为空
  const checkListEmpty = (list: Array<IDataRow>) => {
    if (list.length > 1) {
      return false;
    }

    const [firstRow] = list;
    return !firstRow.clusterData
      && !firstRow.scope
      && firstRow.backupInfos.length < 1;
  };

  const clusterSelectorTabList = [{
    id: ClusterTypes.SPIDER,
    name: '集群',
  }];

  const { t } = useI18n();
  const router = useRouter();
  const { currentBizId } = useGlobalBizs();

  const rowRefs = ref();
  const isShowBatchSelector = ref(false);
  const isSubmitting  = ref(false);

  const tableData = shallowRef<Array<IDataRow>>([createRowData({})]);

  const formData = reactive({
    data_repair: {
      is_repair: true,
      mode: 'manual',
    },
    is_sync_non_innodb: true,
    timing: dayjs().format('YYYY-MM-DD HH:mm:ss'),
    runtime_hour: 48,
  });

  // 批量选择
  const handleShowBatchSelector = () => {
    isShowBatchSelector.value = true;
  };
  // 批量选择
  const handelClusterChange = (selected: {[key: string]: Array<IClusterData>}) => {
    const newList = selected[ClusterTypes.SPIDER].map(clusterData => createRowData({
      clusterData: {
        id: clusterData.id,
        domain: clusterData.master_domain,
      },
    }));
    if (checkListEmpty(tableData.value)) {
      tableData.value = newList;
    } else {
      tableData.value = [...tableData.value, ...newList];
    }
  };
  // 追加一个集群
  const handleAppend = (index: number, appendList: Array<IDataRow>) => {
    const dataList = [...tableData.value];
    dataList.splice(index + 1, 0, ...appendList);
    tableData.value = dataList;
  };
  // 删除一个集群
  const handleRemove = (index: number) => {
    const dataList = [...tableData.value];
    dataList.splice(index, 1);
    tableData.value = dataList;
  };

  const handleSubmit = () => {
    isSubmitting.value = true;
    Promise.all(rowRefs.value.map((item: { getValue: () => Promise<any> }) => item.getValue()))
      .then(data => createTicket({
        ticket_type: 'TENDBCLUSTER_CHECKSUM',
        remark: '',
        details: {
          ...formData,
          infos: data,
        },
        bk_biz_id: currentBizId,
      }))
      .then((data) => {
        window.changeConfirm = false;
        router.push({
          name: 'spiderChecksum',
          params: {
            page: 'success',
          },
          query: {
            ticketId: data.id,
          },
        });
      })
      .finally(() => {
        isSubmitting.value = false;
      });
  };

  const handleReset = () => {
    tableData.value = [createRowData()];
  };
</script>
<style lang="less">
  .spider-manage-checksum-page {
    padding-bottom: 20px;

    .form-block{
      .bk-form-label{
        font-size: 12px;
        font-weight: bold;
        color: #313238;
      }

      .repair-mode-block{
        flex-direction: column;

        .item-box {
          & ~ .item-box {
            margin-top: 20px;
          }

          .item-content {
            position: relative;
            padding-left: 25px;
            font-size: 12px;
            line-height: 20px;
            color: #63656e;
          }

          .item-flag {
            position: absolute;
            left: 3px;
            font-size: 18px;
            color: #979ba5;
          }

          .item-label {
            font-weight: bold;
          }

          .bk-radio {
            align-items: flex-start;

            .bk-radio-input {
              margin-top: 2px;
            }
          }
        }
      }
    }
  }
</style>