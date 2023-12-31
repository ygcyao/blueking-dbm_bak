# Generated by Django 3.2.19 on 2023-07-04 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("redis_dts", "0005_tbtendisdtsjob_unique_dts_job_key"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="tbtendisdtstask",
            constraint=models.UniqueConstraint(
                fields=("bill_id", "src_cluster", "dst_cluster", "src_ip", "src_port"), name="dts_task_unique_key"
            ),
        ),
    ]
