# Generated by Django 2.2.7 on 2020-01-16 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tvvroot', '0018_auto_20200109_0632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='midi_track',
            new_name='midi_track_left_hand',
        ),
    ]