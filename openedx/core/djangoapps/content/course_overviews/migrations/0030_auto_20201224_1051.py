# Generated by Django 2.2.15 on 2020-12-24 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_squashed_0007_historicalorganization'),
        ('course_overviews', '0029_auto_20201222_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_org', to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='historicalcourseoverview',
            name='organization',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='organizations.Organization'),
        ),
    ]
