# Generated by Django 5.0.3 on 2024-04-30 10:19

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_queue_computer'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='queue',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='queue',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]