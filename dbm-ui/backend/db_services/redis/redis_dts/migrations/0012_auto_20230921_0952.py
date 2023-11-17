# Generated by Django 3.2.19 on 2023-09-21 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("redis_dts", "0011_tbtendisdtsjob_online_switch_flow_id_squashed_0015_auto_20230817_1059"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tbtendisdtsjob",
            name="dts_bill_type",
            field=models.CharField(
                choices=[
                    ("REDIS_CLUSTER_SHARD_NUM_UPDATE", "集群节点数变更"),
                    ("REDIS_CLUSTER_TYPE_UPDATE", "集群类型变更"),
                    ("REDIS_CLUSTER_DATA_COPY", "集群数据复制"),
                    ("REDIS_CLUSTER_ROLLBACK_DATA_COPY", "集群回档数据回写"),
                ],
                default="",
                max_length=64,
                verbose_name="DTS单据类型",
            ),
        ),
        migrations.AlterField(
            model_name="tbtendisdtsjob",
            name="dts_copy_type",
            field=models.CharField(
                choices=[
                    ("one_app_diff_cluster", "业务内"),
                    ("diff_app_diff_cluster", "跨业务"),
                    ("copy_to_other_system", "业务内至第三方"),
                    ("user_built_to_dbm", "自建集群至业务内"),
                    ("copy_from_rollback_instance", "构造实例至业务内"),
                ],
                default="",
                max_length=64,
                verbose_name="DTS数据复制类型",
            ),
        ),
    ]