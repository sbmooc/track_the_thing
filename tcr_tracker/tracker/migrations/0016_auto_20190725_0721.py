# Generated by Django 2.2.3 on 2019-07-25 07:21
import django
from django.db import migrations, models


def activate_riders(apps, schema):
    Riders = apps.get_model('tracker', 'Rider')
    Riders.objects.all().update(status='active')

def set_category(apps, schema):
    Riders = apps.get_model('tracker', 'Rider')
    all_riders = Riders.objects.all()
    for rider in all_riders:
        try:
            int(rider.cap_number)
            rider.category = 'Solo'
        except ValueError:
            rider.category = 'Pairs'
        rider.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0015_rider_display_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='rider',
            name='attended_registration_desk',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rider',
            name='gender',
            field=models.CharField(choices=[('M', 'M'), ('F', 'F')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='rider',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('finished', 'Finished'), ('scratched', 'Scratched')], default='active', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='tracker',
            name='working_status',
            field=models.CharField(choices=[
                ('functioning', 'Functioning'),
                ('broken', 'Broken'), ('to_be_tested', 'To Be Tested'), ('lost', 'Lost'), ('unknown', 'Unknown')], max_length=50, null=True, verbose_name='Working Status'),
        ),
        migrations.AlterField(
            model_name='ridercontrolpoint',
            name='rider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='controlpoints', to='tracker.Rider'),
        ),
        migrations.RunPython(
            activate_riders,
            reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name='rider',
            name='cap_number',
            field=models.CharField(max_length=50),
        ),
    ]
