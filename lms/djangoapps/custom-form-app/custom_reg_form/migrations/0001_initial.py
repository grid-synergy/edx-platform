# Generated by Django 2.2.15 on 2020-12-08 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course_overviews', '0026_auto_20201203_0731'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nric', models.CharField(blank=True, max_length=100, null=True, verbose_name='NRIC')),
                ('industry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users_industry', to='course_overviews.Category')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_extra_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
