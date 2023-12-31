# Generated by Django 3.2.19 on 2023-12-04 04:05

from django.db import migrations, models

from backend.db_meta.enums import ClusterType


class Migration(migrations.Migration):

    dependencies = [
        ("open_area", "0002_alter_tendbopenareaconfig_bk_biz_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="tendbopenareaconfig",
            name="cluster_type",
            field=models.CharField(
                choices=ClusterType.get_choices(),
                default="tendbha",
                help_text="开区模板类型[支持tendbha/tendbcluster]",
                max_length=128,
            ),
        ),
    ]
