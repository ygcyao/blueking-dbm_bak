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
  <MainView>
    <template #menu>
      <BkMenu
        :active-key="activeKey"
        :collapse="menuStore.collapsed"
        @click="handleChangeMenu"
        @mouseenter="menuStore.mouseenter"
        @mouseleave="menuStore.mouseleave">
        <div class="main-menu__list db-scroll-y">
          <BkMenuGroup :name="$t('配置管理')">
            <BkMenuItem key="PlatformDbConfigure">
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
                <BkMenuItem key="PlatGlobalStrategy">
                  <template #icon>
                    <i class="db-icon-gaojingcelve" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('全局策略') }}
                  </span>
                </BkMenuItem>
              </FunController>
              <FunController
                controller-id="notice_group"
                module-id="monitor">
                <BkMenuItem key="PlatMonitorAlarmGroup">
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
              <FunController
                controller-id="duty_rule"
                module-id="monitor">
                <BkMenuItem key="PlatRotateSet">
                  <template #icon>
                    <i class="db-icon-db-config" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('轮值策略') }}
                  </span>
                </BkMenuItem>
              </FunController>
              <FunController
                controller-id="monitor_policy"
                module-id="monitor">
                <BkMenuItem key="PlatformNotificationSetting">
                  <template #icon>
                    <i class="db-icon-note" />
                  </template>
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('通知设置') }}
                  </span>
                </BkMenuItem>
              </FunController>
            </BkMenuGroup>
          </FunController>
          <BkMenuGroup :name="$t('巡检')">
            <BkMenuItem key="inspectionManage">
              <template #icon>
                <i class="db-icon-db-config" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('健康报告') }}
              </span>
            </BkMenuItem>
          </BkMenuGroup>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('事件中心')">
            <BkMenuItem key="DBHASwitchEvents">
              <template #icon>
                <i class="db-icon-db-config" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('DBHA切换事件') }}
              </span>
            </BkMenuItem>
          </BkMenuGroup>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('文件管理')">
            <BkMenuItem key="PlatformVersionFiles">
              <template #icon>
                <i class="db-icon-version" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('版本文件') }}
              </span>
            </BkMenuItem>
          </BkMenuGroup>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('资源管理')">
            <BkMenuItem key="ResourceSpecList">
              <template #icon>
                <i class="db-icon-spec" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('资源规格管理') }}
              </span>
            </BkMenuItem>
            <!-- <BkMenuItem key="deploymentPlanManage">
              <template #icon>
                <i class="db-icon-version" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('部署方案') }}
              </span>
            </BkMenuItem> -->
            <BkMenuItem key="resourcePoolManage">
              <template #icon>
                <i class="db-icon-list" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('DB 资源池') }}
              </span>
            </BkMenuItem>
            <BkMenuItem key="resourcePoolDirtyMachines">
              <template #icon>
                <i class="db-icon-dirty-host" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('污点主机处理') }}
              </span>
              <span
                v-if="dirtyHostNums > 0"
                class="main-menu__count">{{ dirtyHostNums > 99 ? '99+' : dirtyHostNums }}</span>
            </BkMenuItem>
          </BkMenuGroup>
          <div class="main-views-space-line" />
          <BkMenuGroup :name="$t('设置')">
            <FunController module-id="mysql">
              <BkSubmenu
                key="platform-mysql"
                title="MySQL">
                <template #icon>
                  <i class="db-icon-mysql" />
                </template>
                <BkMenuItem key="PlatformWhitelist">
                  <!-- <template #icon>
                <i class="db-icon-list" />
              </template> -->
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('授权白名单') }}
                  </span>
                </BkMenuItem>
                <BkMenuItem key="PlatformPasswordPolicy">
                  <!-- <template #icon>
                <i class="db-icon-password" />
              </template> -->
                  <span
                    v-overflow-tips.right
                    class="text-overflow">
                    {{ $t('密码安全规则') }}
                  </span>
                </BkMenuItem>
              </BkSubmenu>
            </FunController>
            <BkMenuItem key="PlatformPasswordRandomization">
              <template #icon>
                <i class="db-icon-pingbi" />
              </template>
              <span
                v-overflow-tips.right
                class="text-overflow">
                {{ $t('密码随机化管理') }}
              </span>
            </BkMenuItem>
            <BkMenuItem key="PlatformStaff">
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
  </MainView>
</template>

<script setup lang="ts">
  import { useMenu } from '@stores';

  import MainView from '@components/layouts/MainView.vue';

  import MenuToggleIcon from '../components/MenuToggleIcon.vue';
  import { useLoopDirtyPool } from '../hooks/useLoopDirtyPool';
  import { useMenuInfo } from '../hooks/useMenuInfo';

  const menuStore = useMenu();
  const { activeKey, handleChangeMenu } = useMenuInfo();
  const dirtyHostNums = useLoopDirtyPool();
</script>
