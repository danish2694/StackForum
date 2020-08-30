# Generated by Django 3.0.3 on 2020-08-26 15:23

import App.models
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answerId', models.CharField(blank=True, max_length=100)),
                ('userId', models.CharField(max_length=50)),
                ('voteType', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionId', models.CharField(blank=True, max_length=100)),
                ('userId', models.CharField(max_length=50)),
                ('voteType', models.IntegerField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserId', models.CharField(blank=True, default='', max_length=50)),
                ('FirstName', models.CharField(blank=True, default='', max_length=50)),
                ('LastName', models.CharField(blank=True, default='', max_length=50)),
                ('Phone', models.CharField(blank=True, default='', max_length=10)),
                ('Age', models.IntegerField(blank=True)),
                ('Password', models.CharField(blank=True, default='', max_length=100)),
                ('Email', models.EmailField(blank=True, max_length=254)),
                ('SecurityQuestion', models.CharField(blank=True, default='', max_length=150)),
                ('SecurityAnswer', models.CharField(blank=True, default='', max_length=500)),
                ('profilePic', models.ImageField(default='media/user.png', upload_to='media')),
                ('Gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questionId', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('question', models.TextField()),
                ('answer', djongo.models.fields.ArrayField(model_container=App.models.Answers, model_form_class=App.models.AnswersForm)),
                ('totalVotes', models.IntegerField(blank=True, default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('Views', models.IntegerField()),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userinfo', to='App.UserDetail')),
            ],
        ),
    ]