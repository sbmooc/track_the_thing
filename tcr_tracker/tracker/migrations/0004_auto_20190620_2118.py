# Generated by Django 2.2.2 on 2019-06-20 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_riders_tracker_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riders',
            name='balance',
            field=models.IntegerField(default=0, null=True),
        ),
    ]