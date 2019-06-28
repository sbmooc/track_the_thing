# Generated by Django 2.2.2 on 2019-06-21 07:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracker', '0005_auto_20190620_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridercheckpoints',
            name='checkpoint',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='riders', to='tracker.Riders'),
        ),
        migrations.AlterField(
            model_name='ridercheckpoints',
            name='rider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='checkpoints', to='tracker.Riders'),
        ),
        migrations.AlterField(
            model_name='riderevents',
            name='rider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='tracker.Riders'),
        ),
        migrations.AlterField(
            model_name='ridernotes',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='tracker.RiderEvents'),
        ),
        migrations.AlterField(
            model_name='ridernotes',
            name='rider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='tracker.Riders'),
        ),
        migrations.AlterField(
            model_name='trackerevents',
            name='tracker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='tracker.Trackers'),
        ),
        migrations.AlterField(
            model_name='trackernotes',
            name='event',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='tracker.TrackerEvents'),
        ),
        migrations.AlterField(
            model_name='trackernotes',
            name='tracker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notes', to='tracker.Trackers'),
        ),
        migrations.AlterField(
            model_name='trackers',
            name='rider_assigned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trackers_assigned', to='tracker.Riders'),
        ),
        migrations.AlterField(
            model_name='trackers',
            name='rider_possess',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trackers_possessed', to='tracker.Riders'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_tcr_staff', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='timestampedmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='tracker.Profile'),
        ),
    ]
