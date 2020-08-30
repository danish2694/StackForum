# Generated by Django 3.0.3 on 2020-08-29 17:09

import App.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_auto_20200826_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blog', djongo.models.fields.EmbeddedField(model_container=App.models.Blog, model_form_class=App.models.BlogForm)),
                ('headline', models.CharField(max_length=255)),
                ('authors', djongo.models.fields.ArrayField(model_container=App.models.Author, model_form_class=App.models.AuthorForm)),
            ],
        ),
    ]
