# Generated by Django 2.2.3 on 2019-07-12 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_auto_20190711_0641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackers',
            name='test_by',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
