# Generated by Django 4.2.13 on 2024-05-09 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='status',
            field=models.IntegerField(choices=[(1, 'Available'), (3, 'In Use'), (4, 'Maintenance')], default=1),
        ),
    ]
