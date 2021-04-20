# Generated by Django 2.2.15 on 2021-01-08 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0032_auto_20210107_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='course_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='courseoverview',
            name='indexed_in_discovery',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcourseoverview',
            name='course_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='historicalcourseoverview',
            name='indexed_in_discovery',
            field=models.BooleanField(default=False),
        ),
    ]
