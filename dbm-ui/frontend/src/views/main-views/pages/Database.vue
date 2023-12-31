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
  <Error v-if="globalBizsStore.isError" />
  <BizPermission v-else-if="notExistBusiness" />
  <MainView v-else>
    <template #menu>
      <BkMenu
        :active-key="activeKey"
        :collapse="menuStore.collapsed"
        :opened-keys="composeOpenKeys"
        @click="handleChangeMenu"
        @mouseenter="menuStore.mouseenter"
        @mouseleave="menuStore.mouseleave">
        <div class="main-menu__list db-scroll-y">
          <AppSelector :collapsed="menuStore.collapsed" />
          <FunController module-id="mysql">
            <BkMenuGroup name="MySQL">
              <FunController
                controller-id="tendbsingle"
                module-id="mysql">
                <BkMenuItem key="DatabaseTendbsingle">
                  <template #icon>
                    <i class="db-icon-node" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('单节点') }}
                  </span>
                </BkMenuItem>
              </FunController>
              <FunController
                controller-id="tendbha"
                module-id="mysql">
                <BkSubmenu
                  key="database-tendbha-cluster"
                  :title="$t('主从')">
                  <template #icon>
                    <i class="db-icon-cluster" />
                  </template>
                  <BkMenuItem key="DatabaseTendbha">
                    <span
                      v-overflow-tips.right
                      class="text-overflow">
                      {{ $t('集群视图') }}
                    </span>
                  </BkMenuItem>
                  <BkMenuItem key="DatabaseTendbhaInstance">
                    <span
                      v-overflow-tips.right
                      class="text-overflow">
                      {{ $t('实例视图') }}
                    </span>
                  </BkMenuItem>
                </BkSubmenu>
              </FunController>
              <BkMenuItem key="mysqlPartitionManage">
                <template #icon>
                  <i class="db-icon-mobanshili" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('分区管理') }}
                </span>
              </BkMenuItem>
              <BkSubmenu
                key="database-permission"
                :title="$t('权限管理')">
                <template #icon>
                  <i class="db-icon-history" />
                </template>
                <BkMenuItem key="PermissionRules">
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('授权规则') }}
                  </span>
                </BkMenuItem>
                <BkMenuItem key="DatabaseWhitelist">
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('授权白名单') }}
                  </span>
                </BkMenuItem>
              </BkSubmenu>
              <BkMenuItem key="DumperDataSubscription">
                <template #icon>
                  <i class="db-icon-mobanshili" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('数据订阅') }}
                </span>
              </BkMenuItem>
              <FunController
                controller-id="toolbox"
                module-id="mysql">
                <li
                  v-show="mysqlToolboxFavorMenus.length > 0"
                  class="main-views-toolbox-split">
                  <span class="split-line" />
                </li>
                <BkSubmenu
                  v-for="group of mysqlToolboxFavorMenus"
                  :key="group.id"
                  :title="group.name">
                  <template #icon>
                    <i :class="group.icon" />
                  </template>
                  <BkMenuItem
                    v-for="item of group.children"
                    :key="item.name">
                    <span
                      v-overflow-tips.right
                      class="text-overflow">
                      {{ item.meta?.navName }}
                    </span>
                  </BkMenuItem>
                </BkSubmenu>
                <BkMenuItem key="MySQLToolbox">
                  <template #icon>
                    <i class="db-icon-tools" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('工具箱') }}
                  </span>
                </BkMenuItem>
              </FunController>
            </BkMenuGroup>
            <div class="main-views-space-line" />
            <FunController
              controller-id="tendbcluster"
              module-id="mysql">
              <BkMenuGroup name="Tendb Cluster">
                <BkSubmenu
                  key="tendb-cluster-manage"
                  :title="$t('TendbCluster集群')">
                  <template #icon>
                    <i class="db-icon-cluster" />
                  </template>
                  <BkMenuItem key="tendbClusterList">
                    <span
                      v-overflow-tips.right
                      class="text-overflow">
                      {{ $t('集群视图') }}
                    </span>
                  </BkMenuItem>
                  <BkMenuItem key="tendbClusterInstance">
                    <span
                      v-overflow-tips.right
                      class="text-overflow">
                      {{ $t('实例视图') }}
                    </span>
                  </BkMenuItem>
                </BkSubmenu>
                <BkMenuItem key="spiderPartitionManage">
                  <template #icon>
                    <i class="db-icon-mobanshili" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('分区管理') }}
                  </span>
                </BkMenuItem>
              </BkMenuGroup>
            </FunController>
            <BkSubmenu
              key="spider-permission"
              :title="$t('权限管理')">
              <template #icon>
                <i class="db-icon-history" />
              </template>
              <BkMenuItem key="spiderPermission">
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('授权规则') }}
                </span>
              </BkMenuItem>
              <!-- <BkMenuItem key="spiderPermissionList">
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('授权列表') }}
                </span>
              </BkMenuItem> -->
              <BkMenuItem key="spiderWhitelist">
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('授权白名单') }}
                </span>
              </BkMenuItem>
            </BkSubmenu>
            <li
              v-show="spiderToolboxFavorMenus.length > 0"
              class="main-views-toolbox-split">
              <span class="split-line" />
            </li>
            <BkSubmenu
              v-for="group of spiderToolboxFavorMenus"
              :key="group.id"
              :title="group.name">
              <template #icon>
                <i :class="group.icon" />
              </template>
              <BkMenuItem
                v-for="item of group.children"
                :key="item.name">
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ item.meta?.navName }}
                </span>
              </BkMenuItem>
            </BkSubmenu>
            <BkMenuItem key="spiderToolbox">
              <template #icon>
                <i class="db-icon-tools" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('工具箱') }}
              </span>
            </BkMenuItem>
          </FunController>
          <div class="main-views-space-line" />
          <FunController module-id="redis">
            <BkMenuGroup name="Redis">
              <BkMenuItem key="RedisManage">
                <template #icon>
                  <i class="db-icon-redis" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('集群管理') }}
                </span>
              </BkMenuItem>
              <FunController
                controller-id="toolbox"
                module-id="redis">
                <li
                  v-show="redisToolboxFavorMenus.length > 0"
                  class="main-views-toolbox-split">
                  <span class="split-line" />
                </li>
                <BkSubmenu
                  v-for="group of redisToolboxFavorMenus"
                  :key="group.id"
                  :title="group.name">
                  <template #icon>
                    <i :class="group.icon" />
                  </template>
                  <BkMenuItem
                    v-for="item of group.children"
                    :key="item.name">
                    <span
                      v-overflow-tips.right
                      class="text-overflow">
                      {{ item.meta?.navName }}
                    </span>
                  </BkMenuItem>
                </BkSubmenu>
                <BkMenuItem key="RedisToolbox">
                  <template #icon>
                    <i class="db-icon-tools" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('工具箱') }}
                  </span>
                </BkMenuItem>
              </FunController>
            </BkMenuGroup>
          </FunController>
          <div class="main-views-space-line" />
          <FunController
            controller-id="es"
            module-id="bigdata">
            <BkMenuGroup name="ES">
              <BkMenuItem key="EsManage">
                <template #icon>
                  <i class="db-icon-es" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('集群管理') }}
                </span>
              </BkMenuItem>
            </BkMenuGroup>
          </FunController>
          <div class="main-views-space-line" />
          <FunController
            controller-id="hdfs"
            module-id="bigdata">
            <BkMenuGroup name="HDFS">
              <BkMenuItem key="HdfsManage">
                <template #icon>
                  <i class="db-icon-hdfs" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('集群管理') }}
                </span>
              </BkMenuItem>
            </BkMenuGroup>
          </FunController>
          <div class="main-views-space-line" />
          <FunController
            controller-id="kafka"
            module-id="bigdata">
            <BkMenuGroup name="Kafka">
              <BkMenuItem key="KafkaManage">
                <template #icon>
                  <i class="db-icon-kafka" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('集群管理') }}
                </span>
              </BkMenuItem>
            </BkMenuGroup>
          </FunController>
          <div class="main-views-space-line" />
          <FunController
            controller-id="pulsar"
            module-id="bigdata">
            <BkMenuGroup name="Pulsar">
              <BkMenuItem key="PulsarManage">
                <template #icon>
                  <i class="db-icon-pulsar" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('集群管理') }}
                </span>
              </BkMenuItem>
            </BkMenuGroup>
          </FunController>
          <div class="main-views-space-line" />
          <FunController
            controller-id="influxdb"
            module-id="bigdata">
            <BkMenuGroup name="InfluxDB">
              <BkMenuItem key="InfluxDBInstances">
                <template #icon>
                  <i class="db-icon-influxdb" />
                </template>
                <span
                  v-overflow-tips.right
                  class="text-overflow">
                  {{ $t('实例管理') }}
                </span>
              </BkMenuItem>
            </BkMenuGroup>
          </FunController>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('配置管理')">
            <BkMenuItem key="DbConfigure">
              <template #icon>
                <i class="db-icon-db-config" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('数据库配置') }}
              </span>
            </BkMenuItem>
          </BkMenuGroup>
          <div class="main-views-space-line" />
          <FunController module-id="monitor">
            <BkMenuGroup :name="$t('监控告警')">
              <FunController
                controller-id="monitor_policy"
                module-id="monitor">
                <BkMenuItem key="DBMonitorStrategy">
                  <template #icon>
                    <i class="db-icon-gaojingcelve" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('监控策略') }}
                  </span>
                </BkMenuItem>
              </FunController>
              <FunController
                controller-id="notice_group"
                module-id="monitor">
                <BkMenuItem key="DBMonitorAlarmGroup">
                  <template #icon>
                    <i class="db-icon-yonghuzu" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('告警组') }}
                  </span>
                </BkMenuItem>
              </FunController>
            </BkMenuGroup>
          </FunController>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('任务中心')">
            <BkMenuItem key="taskHistory">
              <template #icon>
                <i class="db-icon-history" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('历史任务') }}
              </span>
            </BkMenuItem>
          </BkMenuGroup>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('安全')">
            <BkMenuItem key="DBPasswordTemporaryModify">
              <template #icon>
                <i class="db-icon-password" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('修改密码') }}
              </span>
            </BkMenuItem>
          </BkMenuGroup>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('设置')">
            <BkMenuItem key="DatabaseStaff">
              <template #icon>
                <i class="db-icon-dba-config" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('DBA人员管理') }}
              </span>
            </BkMenuItem>
          </BkMenuGroup>
        </div>
        <MenuToggleIcon />
      </BkMenu>
    </template>
    <template
      v-if="!biz?.permission?.db_manage"
      #main-content>
      <BizPermission />
    </template>
  </MainView>
</template>

<script setup lang="ts">
  import type { Emitter } from 'mitt';
  import mitt from 'mitt';
  import type { RouteRecordRaw } from 'vue-router';

  import { useGlobalBizs, useMenu, useUserProfile  } from '@stores';

  import { UserPersonalSettings } from '@common/const';

  import AppSelector from '@components/app-selector/index.vue';
  import MainView from '@components/layouts/MainView.vue';

  import BizPermission from '@views/exception/BizPermission.vue';
  import Error from '@views/exception/Error.vue';
  import { mysqlToolboxChildrenRouters } from '@views/mysql/routes';
  import mysqlToolboxMenus, { type MenuChild } from '@views/mysql/toolbox/common/menus';
  import { redisToolboxChildrenRoutes } from '@views/redis/routes';
  import redisToolboxMenus from '@views/redis/toolbox/common/menus';
  import { spiderToolboxChildrenRoutes } from '@views/spider-manage/routes';
  import spiderToolboxMenus from '@views/spider-manage/toolbox/common/menus';

  import MenuToggleIcon from '../components/MenuToggleIcon.vue';
  import { useMenuInfo } from '../hooks/useMenuInfo';

  interface ToolboxMenuGroup {
    children: RouteRecordRaw[];
    name: string;
    id: string;
    icon: string;
  }

  type MenuList = typeof mysqlToolboxMenus;

  function generateToolboxFavorMenus(type: 'mysql' | 'redis' | 'spider') {
    let favors: Array<MenuChild> = [];
    let toolboxChildrenRouters: RouteRecordRaw[] = [];
    let toolBoxMenus: MenuList = [];
    switch (type) {
    case 'mysql':
      favors = userProfileStore.profile[UserPersonalSettings.MYSQL_TOOLBOX_FAVOR] || [];
      toolboxChildrenRouters = mysqlToolboxChildrenRouters;
      toolBoxMenus = mysqlToolboxMenus;
      break;
    case 'redis':
      favors = userProfileStore.profile[UserPersonalSettings.REDIS_TOOLBOX_FAVOR] || [];
      toolboxChildrenRouters = redisToolboxChildrenRoutes;
      toolBoxMenus = redisToolboxMenus;
      break;
    default:
      favors = userProfileStore.profile[UserPersonalSettings.SPIDER_TOOLBOX_FAVOR] || [];
      toolboxChildrenRouters = spiderToolboxChildrenRoutes;
      toolBoxMenus = spiderToolboxMenus;
      break;
    }
    if (favors.length === 0) return [];

    const menuGroup: ToolboxMenuGroup[] = toolBoxMenus.map(item => ({
      ...item,
      children: [],
    }));
    const routesMap: Record<string, Array<RouteRecordRaw>> = {};
    for (const item of favors) {
      const curRoute = toolboxChildrenRouters.find(toolboxRoute => toolboxRoute.name === item.id);
      if (curRoute && routesMap[item.parentId]) {
        routesMap[item.parentId].push(curRoute);
      } else if (curRoute) {
        routesMap[item.parentId] = [curRoute];
      }
      // 动态设置 activeMenu
      if (curRoute?.meta) {
        curRoute.meta.activeMenu = undefined;
      }
    }

    for (const key of Object.keys(routesMap)) {
      const menus = menuGroup.find(item => item.id === key);
      if (menus) {
        menus.children = routesMap[key];
      }
    }
    return menuGroup.filter(item => item.children.length > 0);
  }

  const eventBus = mitt() as Emitter<any>;
  provide('collapseEventBus', eventBus);

  const menuStore = useMenu();
  const route = useRoute();
  const globalBizsStore = useGlobalBizs();
  const userProfileStore = useUserProfile();
  const { activeKey, handleChangeMenu, openedKeys } = useMenuInfo();

  const addOpenKey = ref('');

  const composeOpenKeys = computed(() => [...openedKeys.value, addOpenKey.value]);
  const biz = computed(() => globalBizsStore.bizs.find(item => item.bk_biz_id === Number(route.params.bizId)));
  const notExistBusiness = computed(() => globalBizsStore.bizs.length === 0 && !biz.value);

  // Mysql工具箱收藏导航
  const mysqlToolboxFavorMenus = computed(() => generateToolboxFavorMenus('mysql'));

  // Redis工具箱收藏导航
  const redisToolboxFavorMenus = computed(() => generateToolboxFavorMenus('redis'));

  // Spider工具箱收藏导航
  const spiderToolboxFavorMenus = computed(() => generateToolboxFavorMenus('spider'));

  watch(activeKey, () => {
    handleToggleCollapse('');
  });

  const handleToggleCollapse = (key: string) => {
    addOpenKey.value = key;
  };

  eventBus.on('collapse', handleToggleCollapse);

  onBeforeUnmount(() => {
    eventBus.off('collapse', handleToggleCollapse);
  });
</script>

<style lang="less">
.main-views-toolbox-split {
  width: 100%;
  height: 0;
  padding: 0 20px 0 60px;

  .split-line {
    display: inline-block;
    width: 100%;
    margin-bottom: 15px;
    border-bottom: solid #29344c 1px;
  }
}

.main-views-space-line {
  width: 100%;
  height: 16px;
}
</style>
