# Generated by Django 2.2.7 on 2020-01-20 18:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tvvroot', '0026_instrumentmap_limbs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='music',
            old_name='audio',
            new_name='audio_file',
        ),
        migrations.RenameField(
            model_name='music',
            old_name='midi',
            new_name='midi_file',
        ),
        migrations.CreateModel(
            name='MIDI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('track_number', models.PositiveSmallIntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvvroot.Music')),
            ],
        ),
    ]