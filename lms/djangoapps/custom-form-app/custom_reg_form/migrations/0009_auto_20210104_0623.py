# Generated by Django 2.2.15 on 2021-01-04 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_reg_form', '0008_auto_20210104_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextrainfo',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users_industry', to='course_overviews.Category'),
        ),
    ]
