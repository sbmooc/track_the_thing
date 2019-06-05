# Generated by Django 2.2.2 on 2019-06-05 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RiderEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('event_type', models.CharField(choices=[('payment_in', 'Payment In'), ('payment_out', 'Payment Out'), ('start_race', 'Start Race'), ('finish_race', 'Finish Race'), ('scratch', 'Scratch'), ('arrive_checkpoint', 'Arrive Checkpoint')], max_length=50)),
                ('balance_change', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Riders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('cap_number', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('pair', 'Pair')], max_length=50)),
                ('balance', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TrackerEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('event_type', models.CharField(choices=[('tested_OK', 'Tested OK'), ('tested_broken', 'Tested Broken'), ('add_tracker_assignment', 'Tracker add assignment'), ('remove_tracker_assignment', 'Tracker remove assignment'), ('add_tracker_possession', 'Tracker add possession'), ('remove_tracker_possession', 'Tracker remove possession')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Trackers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('esn_number', models.CharField(max_length=50)),
                ('working_status', models.CharField(choices=[('working', 'Working'), ('broken', 'Broken'), ('to_be_tested', 'To Be Tested'), ('unknown', 'Unknown')], max_length=50)),
                ('loan_status', models.CharField(choices=[('with_rider', 'With Rider'), ('not_loaned', 'Not Loaned'), ('other', 'Other')], max_length=50)),
                ('last_test_date', models.DateField(null=True)),
                ('purchase_date', models.DateField(null=True)),
                ('warranty_expiry', models.DateField(null=True)),
                ('owner', models.CharField(choices=[('lost_dot', 'Lost Dot'), ('rider_owned', 'Rider Owned'), ('third_party', 'Third Party')], max_length=50)),
                ('rider_assigned', models.ManyToManyField(related_name='assigned_trackers', to='tracker.Riders')),
                ('rider_possess', models.ManyToManyField(related_name='possessed_trackers', to='tracker.Riders')),
            ],
        ),
        migrations.CreateModel(
            name='TrackerNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('notes', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='tracker.TrackerEvents')),
                ('tracker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='tracker.Trackers')),
            ],
        ),
        migrations.AddField(
            model_name='trackerevents',
            name='tracker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='tracker.Trackers'),
        ),
        migrations.CreateModel(
            name='RiderNotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('notes', models.TextField()),
                ('events', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='tracker.RiderEvents')),
                ('rider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='tracker.Riders')),
            ],
        ),
        migrations.AddField(
            model_name='riderevents',
            name='rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='tracker.Riders'),
        ),
    ]
