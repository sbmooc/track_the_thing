# Generated by Django 2.2.3 on 2019-10-01 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0025_auto_20190930_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='race',
            field=models.CharField(choices=[('TCR', 'TCR'), ('TPR', 'TPR')], default='TPR', max_length=50, null=True),
        ),
    ]
