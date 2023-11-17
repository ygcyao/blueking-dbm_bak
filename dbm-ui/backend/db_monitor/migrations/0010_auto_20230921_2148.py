# Generated by Django 3.2.19 on 2023-09-21 13:48

from django.db import migrations, models

from backend.configuration.constants import DBType
from backend.db_monitor.constants import DutyRuleCategory


class Migration(migrations.Migration):

    dependencies = [
        ("db_monitor", "0009_remove_monitorpolicy_expected_notify_groups"),
    ]

    operations = [
        migrations.CreateModel(
            name="DutyRule",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creator", models.CharField(max_length=64, verbose_name="创建人")),
                ("create_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updater", models.CharField(max_length=64, verbose_name="修改人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("name", models.CharField(max_length=255, verbose_name="轮值规则名称")),
                ("priority", models.PositiveIntegerField(verbose_name="优先级")),
                ("is_enabled", models.BooleanField(default=True, verbose_name="是否启用")),
                ("effective_time", models.DateTimeField(verbose_name="生效时间")),
                ("end_time", models.DateTimeField(blank=True, null=True, verbose_name="截止时间")),
                (
                    "category",
                    models.CharField(choices=DutyRuleCategory.get_choices(), max_length=32, verbose_name="轮值类型"),
                ),
                (
                    "db_type",
                    models.CharField(
                        choices=DBType.get_choices(),
                        max_length=32,
                        verbose_name="数据库类型",
                    ),
                ),
                ("duty_arranges", models.JSONField(verbose_name="轮值人员设置")),
            ],
            options={
                "verbose_name": "轮值规则",
                "verbose_name_plural": "轮值规则",
            },
        ),
        migrations.AlterModelOptions(
            name="noticegroup",
            options={"verbose_name": "告警通知组", "verbose_name_plural": "告警通知组"},
        ),
    ]