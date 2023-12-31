# Generated by Django 3.2.19 on 2023-06-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configuration", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FunctionController",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255, verbose_name="功能名称")),
                ("is_enabled", models.BooleanField(default=False, verbose_name="是否开启")),
                ("is_frozen", models.BooleanField(default=False, help_text="人工冻结此开关，将不受更新影响", verbose_name="是否冻结")),
                ("parent_name", models.CharField(blank=True, max_length=255, null=True, verbose_name="父功能名称")),
            ],
            options={
                "verbose_name": "功能控制器",
                "verbose_name_plural": "功能控制器",
                "unique_together": {("name", "parent_name")},
            },
        ),
    ]
