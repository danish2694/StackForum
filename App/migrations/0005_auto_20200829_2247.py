# Generated by Django 3.0.3 on 2020-08-29 17:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_entry'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questions',
            old_name='answer',
            new_name='answers',
        ),
    ]