import type { RouteRecordRaw } from 'vue-router';

import { t } from '@locales/index';

export default (): RouteRecordRaw[] => [
  {
    name: 'serviceApply',
    path: 'service-apply',
    meta: {
      navName: t('服务申请'),
    },
    redirect: {
      name: 'serviceApplyIndex',
    },
    children: [
      {
        name: 'serviceApplyIndex',
        path: 'index',
        component: () => import('@views/service-apply/index/Index.vue'),
        meta: {
          navName: t('服务申请'),
        },
      },
      {
        name: 'SelfServiceApplySingle',
        path: 'single',
        meta: {
          navName: t('申请MySQL单节点部署'),
        },
        component: () => import('@views/mysql/apply/ApplyMySQL.vue'),
      },
      {
        name: 'SelfServiceApplyHa',
        path: 'ha',
        meta: {
          navName: t('申请MySQL主从部署'),
        },
        component: () => import('@views/mysql/apply/ApplyMySQL.vue'),
      },
      {
        name: 'spiderApply',
        path: 'tendbcluster',
        meta: {
          navName: t('申请TendbCluster分布式集群部署'),
        },
        component: () => import('@views/spider-manage/apply/Index.vue'),
      },
      {
        name: 'SelfServiceApplyRedis',
        path: 'redis',
        meta: {
          navName: t('申请Redis集群部署'),
        },
        component: () => import('@views/redis/apply/ApplyRedis.vue'),
      },
      {
        name: 'EsApply',
        path: 'es',
        meta: {
          navName: t('申请ES集群部署'),
        },
        component: () => import('@views/es-manage/apply/Index.vue'),
      },
      {
        name: 'KafkaApply',
        path: 'kafka',
        meta: {
          navName: t('申请Kafka集群部署'),
        },
        component: () => import('@views/kafka-manage/apply/Index.vue'),
      },
      {
        name: 'HdfsApply',
        path: 'hdfs',
        meta: {
          navName: t('申请HDFS集群部署'),
        },
        component: () => import('@views/hdfs-manage/apply/Index.vue'),
      },
      {
        name: 'PulsarApply',
        path: 'pulsar',
        meta: {
          navName: t('申请Pulsar集群部署'),
        },
        component: () => import('@views/pulsar-manage/apply/index.vue'),
      },
      {
        name: 'SelfServiceApplyInfluxDB',
        path: 'influxdb',
        meta: {
          navName: t('申请InfluxDB集群部署'),
        },
        component: () => import('@views/influxdb-manage/apply/index.vue'),
      },
      {
        name: 'SelfServiceCreateDbModule',
        path: 'create-db-module/:type/:bk_biz_id/',
        meta: {
          navName: t('新建模块'),
        },
        component: () => import('@views/service-apply/create-db-module/Index.vue'),
      },
      {
        name: 'SelfServiceBindDbModule',
        path: 'bind-db-module/:type/:bk_biz_id/:db_module_id',
        meta: {
          navName: t('绑定配置'),
        },
        component: () => import('@views/service-apply/create-db-module/Index.vue'),
      },
    ],
  },
];
