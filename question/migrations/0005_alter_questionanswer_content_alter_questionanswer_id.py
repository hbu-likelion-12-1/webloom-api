# Generated by Django 5.0.7 on 2024-07-23 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question", "0004_alter_question_female_audio_url_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="questionanswer",
            name="content",
            field=models.CharField(db_comment="마음 게시글 본문", max_length=200),
        ),
        migrations.AlterField(
            model_name="questionanswer",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
