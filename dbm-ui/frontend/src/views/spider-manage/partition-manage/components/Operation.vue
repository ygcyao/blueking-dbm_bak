<template>
  <div class="partition-operation-box">
    <BkAlert
      class="mb-16"
      theme="info">
      <div>{{ t('如果已经是分区表，会维护新分区，理论上不影响业务') }}</div>
      <div>{{ t('如果不是分区表，会转换成分区表，存在表数据迁移到新表，理论上不影响业务') }}</div>
      <div>{{ t('如果大于 500G 的表，无法执行分区') }}</div>
      <div>{{ t('建议在低峰期执行') }}</div>
    </BkAlert>
    <DbForm
      ref="formRef"
      form-type="vertical"
      :model="formData"
      :rules="rules">
      <DbFormItem
        :label="t('目标集群')"
        property="cluster_id"
        required>
        <BkSelect
          :loading="isCluserListLoading"
          :model-value="formData.cluster_id || undefined"
          @change="handleClusterChange">
          <BkOption
            v-for="item in clusterList?.results"
            :id="item.id"
            :key="item.id"
            :name="item.cluster_name" />
        </BkSelect>
      </DbFormItem>
      <DbFormItem
        :label="t('目标 DB')"
        property="dblikes"
        required>
        <BkTagInput
          v-model="formData.dblikes"
          allow-create
          :max-data="1" />
      </DbFormItem>
      <DbFormItem
        :label="t('目标表')"
        property="tblikes"
        required>
        <BkTagInput
          v-model="formData.tblikes"
          allow-create
          :max-data="1" />
      </DbFormItem>
      <DbFormItem
        :label="t('字段类型')"
        property="partition_column_type"
        required>
        <BkSelect v-model="formData.partition_column_type">
          <BkOption
            id="int"
            name="整型" />
          <BkOption
            id="datetime"
            name="日期类型" />
          <BkOption
            id="timestamp"
            name="时间戳类型" />
        </BkSelect>
      </DbFormItem>
      <DbFormItem
        :label="t('分区字段')"
        property="partition_column"
        required>
        <BkInput v-model="formData.partition_column" />
      </DbFormItem>
      <DbFormItem
        :label="t('分区间隔')"
        property="partition_time_interval"
        required>
        <BkInput
          v-model="formData.partition_time_interval"
          :min="1"
          :suffix="t('天')"
          type="number" />
      </DbFormItem>
      <DbFormItem
        :label="t('数据过期时间')"
        property="expire_time"
        required>
        <BkInput
          v-model="formData.expire_time"
          :min="1"
          :suffix="t('天')"
          type="number" />
      </DbFormItem>
    </DbForm>
  </div>
</template>
<script setup lang="ts">
  import {
    reactive,
    watch,
  } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { useRequest } from 'vue-request';

  import type PartitionModel from '@services/model/partition/partition';
  import {
    create as createParitition,
    edit as editPartition,
    verifyPartitionField,
  } from '@services/partitionManage';
  import { getList } from '@services/spider';

  interface Props {
    data?: PartitionModel
  }
  interface Expose {
    submit: () => Promise<any>
  }

  const props = defineProps<Props>();

  const { t } = useI18n();

  const formRef = ref();
  const formData = reactive({
    cluster_id: 0,
    dblikes: [] as string[],
    tblikes: [] as string[],
    partition_column: '',
    partition_column_type: 'int',
    expire_time: 7,
    partition_time_interval: 420,
  });

  const rules = {
    dblikes: [
      {
        required: true,
        validator: (value: string[]) => value.length > 0,
        message: t('目标 DB 不能为空'),
        trigger: 'change',
      },
    ],
    tblikes: [
      {
        required: true,
        validator: (value: string[]) => value.length > 0,
        message: t('目标 DB 不能为空'),
        trigger: 'change',
      },
    ],
    partition_column: [
      {
        validator: (value: string) => verifyPartitionField({
          cluster_id: formData.cluster_id,
          dblikes: formData.dblikes,
          tblikes: formData.tblikes,
          partition_column: value,
          partition_column_type: formData.partition_column_type,
        }),
        trigger: 'blur',
      },
    ],
  };

  const {
    loading: isCluserListLoading,
    data: clusterList,
  } = useRequest(getList, {
    defaultParams: [{
      limit: -1,
    }],
  });

  watch(() => props.data, () => {
    if (props.data) {
      formData.cluster_id = props.data.cluster_id;
      formData.dblikes = [props.data.dblike];
      formData.tblikes = [props.data.tblike];
      formData.partition_column = props.data.partition_columns;
      formData.partition_column_type = props.data.partition_column_type;
      formData.expire_time = props.data.expire_time;
      formData.partition_time_interval = props.data.partition_time_interval;
    }
  }, {
    immediate: true,
  });

  const handleClusterChange = (value: number) => {
    formData.cluster_id = value;
  };

  defineExpose<Expose>({
    submit() {
      return formRef.value.validate()
        .then(() => {
          if (props.data) {
            return editPartition({
              id: props.data.id,
              ...formData,
            });
          }

          return createParitition({
            ...formData,
          });
        });
    },
  });
</script>
<style lang="less">
  .partition-operation-box {
    padding: 20px 40px;
  }
</style>