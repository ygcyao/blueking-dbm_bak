# Generated by Django 3.2.19 on 2023-11-20 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("db_monitor", "0017_auto_20231102_2100"),
    ]

    operations = [
        migrations.AddField(
            model_name="dashboard",
            name="view",
            field=models.CharField(default="集群监控视图", max_length=128, verbose_name="视图类型"),
        ),
        migrations.AlterUniqueTogether(
            name="dashboard",
            unique_together={("name", "view")},
        ),
    ]
