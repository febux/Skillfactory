# Generated by Django 3.1.7 on 2021-03-27 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SlackUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_user', models.TextField(unique=True)),
                ('slack_category_post', models.ManyToManyField(blank=True, to='actions.Category')),
            ],
        ),
    ]
