# Generated by Django 3.2.19 on 2023-11-21 13:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("configuration", "0007_auto_20231121_1950"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bizsettings",
            options={
                "ordering": ("id",),
                "verbose_name": "业务配置(BizSettings)",
                "verbose_name_plural": "业务配置(BizSettings)",
            },
        ),
        migrations.AlterModelOptions(
            name="dbadministrator",
            options={"verbose_name": "DBA人员设置(DBAdministrator)", "verbose_name_plural": "DBA人员设置(DBAdministrator)"},
        ),
        migrations.AlterModelOptions(
            name="functioncontroller",
            options={"verbose_name": "功能控制器(FunctionController)", "verbose_name_plural": "功能控制器(FunctionController)"},
        ),
        migrations.AlterModelOptions(
            name="ipwhitelist",
            options={"verbose_name": "IP白名单(IPWhitelist)", "verbose_name_plural": "IP白名单(IPWhitelist)"},
        ),
        migrations.AlterModelOptions(
            name="passwordpolicy",
            options={"verbose_name": "密码安全策略(PasswordPolicy)", "verbose_name_plural": "密码安全策略(PasswordPolicy)"},
        ),
        migrations.AlterModelOptions(
            name="profile",
            options={"verbose_name": "个人偏好(Profile)", "verbose_name_plural": "个人偏好(Profile)"},
        ),
        migrations.AlterModelOptions(
            name="systemsettings",
            options={
                "ordering": ("id",),
                "verbose_name": "系统配置(SystemSettings)",
                "verbose_name_plural": "系统配置(SystemSettings)",
            },
        ),
    ]
