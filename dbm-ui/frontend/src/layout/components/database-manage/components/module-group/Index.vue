<template>
  <component :is="renderCom" />
</template>
<script setup lang="ts">
  import { computed } from 'vue';

  import Es from './Es.vue';
  import Hdfs from './Hdfs.vue';
  import Influxdb from './Influxdb.vue';
  import Kafka from './Kafka.vue';
  import Mysql from './Mysql.vue';
  import Pulsar from './Pulsar.vue';
  import Redis from './Redis.vue';
  import TendbCluster from './TendbCluster.vue';

  interface Props {
    name: string
  }

  const props = defineProps<Props>();

  const comMap = {
    es: Es,
    hdfs: Hdfs,
    influxdb: Influxdb,
    kafka: Kafka,
    mysql: Mysql,
    pulsar: Pulsar,
    redis: Redis,
    tendbCluster: TendbCluster,
  };

  const renderCom = computed(() => comMap[props.name as keyof typeof comMap]);
</script>

