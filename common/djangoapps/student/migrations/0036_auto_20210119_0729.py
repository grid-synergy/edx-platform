# Generated by Django 2.2.15 on 2021-01-19 07:29

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0035_auto_20210104_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='SG', max_length=2, null=True),
        ),
    ]
