# Generated by Django 3.2.3 on 2021-05-25 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_post_image_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_post',
            field=models.ImageField(blank=True, null=True, upload_to='media/uploads/'),
        ),
    ]
