# Generated by Django 5.0.7 on 2024-07-27 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_remove_userdepressiontest_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfertility",
            name="care_status",
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name="userinfertility",
            name="cause",
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name="userinfertility",
            name="communication",
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name="userinfertility",
            name="cost",
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name="userinfertility",
            name="period",
            field=models.CharField(),
        ),
        migrations.AlterField(
            model_name="userinfertility",
            name="workplace_comprehension",
            field=models.CharField(),
        ),
    ]
