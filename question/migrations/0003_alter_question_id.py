# Generated by Django 5.0.7 on 2024-07-21 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
