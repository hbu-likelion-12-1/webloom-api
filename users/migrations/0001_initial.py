# Generated by Django 5.0.7 on 2024-07-20 01:49

import app.enum
import app.orm
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(
                    max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("kakao_id", models.CharField(max_length=50)),
                ("username", models.CharField(max_length=10)),
                ("sex", models.CharField(max_length=1)),
                ("region", models.CharField(max_length=20)),
                ("city", models.CharField(max_length=20)),
                ("town", models.CharField(max_length=20)),
                ("birthday", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        related_name="custom_user_groups", to="auth.group"
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        related_name="custom_user_permissions", to="auth.permission"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserDepressionTest",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("json", models.JSONField()),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_depression_test",
                        to="users.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserInfertility",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("period", app.orm.TextEnumField(enum=app.enum.InferPeriod)),
                ("care_status", app.orm.TextEnumField(
                    enum=app.enum.InferCareStatus)),
                ("cause", app.orm.TextEnumField(enum=app.enum.InferCause)),
                ("cost", app.orm.TextEnumField(enum=app.enum.InferCost)),
                (
                    "workplace_comprehension",
                    app.orm.TextEnumField(
                        enum=app.enum.WorkplaceComprehension),
                ),
                (
                    "communication",
                    app.orm.TextEnumField(enum=app.enum.InferCommunication),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_infertility",
                        to="users.user",
                    ),
                ),
            ],
        ),
    ]
