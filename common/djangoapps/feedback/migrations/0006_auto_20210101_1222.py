# Generated by Django 2.2.15 on 2021-01-01 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_auto_20210101_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursereview',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]
