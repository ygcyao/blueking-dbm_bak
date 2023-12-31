# Generated by Django 3.2.19 on 2023-08-29 02:33

from django.db import migrations, models

from backend.configuration.constants import DBType
from backend.db_monitor.constants import PolicyStatus, TargetLevel


class Migration(migrations.Migration):

    dependencies = [
        ("db_monitor", "0003_alter_noticegroup_db_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="DispatchGroup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creator", models.CharField(max_length=64, verbose_name="创建人")),
                ("create_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updater", models.CharField(max_length=64, verbose_name="修改人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("monitor_dispatch_id", models.IntegerField(default=0, verbose_name="蓝鲸监控分派策略组ID")),
                ("name", models.CharField(max_length=128, verbose_name="策略名称，全局唯一")),
                ("priority", models.PositiveIntegerField(verbose_name="监控策略优先级，跟随targets调整")),
                ("details", models.JSONField(default=dict, verbose_name="策略模板详情，可用于还原")),
                ("is_synced", models.BooleanField(default=False, verbose_name="是否已同步到监控")),
                ("sync_at", models.DateTimeField(null=True, verbose_name="最近一次的同步时间")),
            ],
            options={
                "verbose_name": "分派策略组",
            },
        ),
        migrations.CreateModel(
            name="MonitorPolicy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creator", models.CharField(max_length=64, verbose_name="创建人")),
                ("create_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updater", models.CharField(max_length=64, verbose_name="修改人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("parent_id", models.IntegerField(default=0, verbose_name="父级策略ID，0代表父级")),
                ("name", models.CharField(max_length=128, unique=True, verbose_name="策略名称，全局唯一")),
                ("bk_biz_id", models.IntegerField(default=0, verbose_name="业务ID, 0代表全业务")),
                (
                    "db_type",
                    models.CharField(
                        choices=DBType.get_choices(),
                        default="mysql",
                        max_length=64,
                        verbose_name="DB类型",
                    ),
                ),
                ("details", models.JSONField(default=dict, verbose_name="策略模板详情，可用于还原")),
                ("targets", models.JSONField(default=dict, verbose_name="监控目标")),
                (
                    "target_level",
                    models.CharField(
                        choices=TargetLevel.get_choices(),
                        default="APP",
                        max_length=64,
                        verbose_name="监控目标级别，跟随targets调整",
                    ),
                ),
                ("target_priority", models.PositiveIntegerField(verbose_name="监控策略优先级，跟随targets调整")),
                ("test_rules", models.JSONField(default=dict, verbose_name="检测规则")),
                ("notify_rules", models.JSONField(default=dict, verbose_name="通知规则")),
                ("notify_groups", models.JSONField(default=dict, verbose_name="通知组")),
                ("is_enabled", models.BooleanField(default=True, verbose_name="是否已启用")),
                ("is_synced", models.BooleanField(default=False, verbose_name="是否已同步到监控")),
                ("sync_at", models.DateTimeField(null=True, verbose_name="最近一次的同步时间")),
                ("event_count", models.IntegerField(default=-1, verbose_name="告警事件数量，初始值设置为-1")),
                (
                    "policy_status",
                    models.CharField(
                        choices=PolicyStatus.get_choices(),
                        default="valid",
                        max_length=64,
                        verbose_name="策略状态",
                    ),
                ),
                ("dispatch_group_id", models.BigIntegerField(default=0, verbose_name="分派策略组ID，0代表没有对应的策略")),
                ("monitor_policy_id", models.BigIntegerField(default=0, verbose_name="蓝鲸监控策略ID")),
            ],
            options={
                "verbose_name": "告警策略",
            },
        ),
        migrations.RemoveField(
            model_name="noticegroup",
            name="users",
        ),
        migrations.AddField(
            model_name="noticegroup",
            name="details",
            field=models.JSONField(default=dict, verbose_name="通知方式详情"),
        ),
        migrations.AddField(
            model_name="noticegroup",
            name="is_synced",
            field=models.BooleanField(default=False, verbose_name="是否已同步到监控"),
        ),
        migrations.AddField(
            model_name="noticegroup",
            name="receivers",
            field=models.JSONField(default=dict, verbose_name="告警接收人员/组列表"),
        ),
        migrations.AddField(
            model_name="noticegroup",
            name="sync_at",
            field=models.DateTimeField(null=True, verbose_name="最近一次的同步时间"),
        ),
        migrations.AlterField(
            model_name="ruletemplate",
            name="name",
            field=models.CharField(max_length=128, unique=True, verbose_name="策略名称监控侧要求唯一"),
        ),
    ]
