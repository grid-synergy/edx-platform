# Generated by Django 2.2.20 on 2021-05-17 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lhub_ecommerce_offer', '0003_auto_20210511_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
