# Generated by Django 3.2.19 on 2023-09-07 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TendbOpenAreaConfigLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creator", models.CharField(max_length=64, verbose_name="创建人")),
                ("create_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updater", models.CharField(max_length=64, verbose_name="修改人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("bk_biz_id", models.IntegerField(default=0)),
                ("config_name", models.CharField(default="", max_length=256)),
                ("config_change_log", models.JSONField(help_text="开区配置修改记录数据")),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TendbOpenAreaConfig",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creator", models.CharField(max_length=64, verbose_name="创建人")),
                ("create_at", models.DateTimeField(auto_now_add=True, verbose_name="创建时间")),
                ("updater", models.CharField(max_length=64, verbose_name="修改人")),
                ("update_at", models.DateTimeField(auto_now=True, verbose_name="更新时间")),
                ("bk_biz_id", models.IntegerField(default=0, help_text="业务ID")),
                ("config_name", models.CharField(help_text="开区模板名", max_length=256)),
                ("source_cluster_id", models.BigIntegerField(help_text="源集群ID")),
                ("config_rules", models.JSONField(help_text="模板克隆规则列表")),
                ("related_authorize", models.JSONField(help_text="关联的规则列表(目前用于级联规则的修改删除)")),
            ],
            options={
                "unique_together": {("bk_biz_id", "config_name")},
            },
        ),
    ]
