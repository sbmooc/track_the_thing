# Generated by Django 2.2.3 on 2019-07-13 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0011_auto_20190712_1706'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ControlPoints',
            new_name='ControlPoint',
        ),
        migrations.RenameModel(
            old_name='Events',
            new_name='Event',
        ),
        migrations.RenameModel(
            old_name='Riders',
            new_name='Rider',
        ),
        migrations.RenameModel(
            old_name='RiderControlPoints',
            new_name='RiderControlPoint',
        ),
        migrations.RenameModel(
            old_name='Trackers',
            new_name='Tracker',
        ),
    ]
