# Generated by Django 2.2.3 on 2019-09-30 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0023_event_race'),
    ]

    operations = [
        migrations.AddField(
            model_name='rider',
            name='offset',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
