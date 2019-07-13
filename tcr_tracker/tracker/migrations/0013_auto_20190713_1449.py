# Generated by Django 2.2.3 on 2019-07-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0012_auto_20190713_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='working_status',
            field=models.CharField(choices=[('working', 'Working'), ('broken', 'Broken'), ('to_be_tested', 'To Be Tested'), ('lost', 'Lost'), ('unknown', 'Unknown')], max_length=50, null=True, verbose_name='Working Status'),
        ),
    ]