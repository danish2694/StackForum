# Generated by Django 3.0.3 on 2020-07-25 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_entry_questions_userdetail_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votes',
            name='questionId',
            field=models.CharField(max_length=100),
        ),
    ]
