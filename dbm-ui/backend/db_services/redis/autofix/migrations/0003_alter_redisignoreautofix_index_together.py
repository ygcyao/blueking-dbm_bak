# Generated by Django 3.2.19 on 2023-12-19 07:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("autofix", "0002_auto_20231120_1955"),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name="redisignoreautofix",
            index_together={("bk_biz_id", "ip")},
        ),
    ]
