# Generated by Django 2.2.15 on 2020-12-03 13:29

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('terms_conditions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termsconditions',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
