# Generated by Django 2.2.18 on 2021-04-20 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0002_auto_20210420_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='banner_img',
            field=models.ImageField(upload_to='banner/lms/courses'),
        ),
    ]
