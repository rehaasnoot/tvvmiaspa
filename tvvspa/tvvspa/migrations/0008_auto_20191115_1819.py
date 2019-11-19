# Generated by Django 2.2.7 on 2019-11-15 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tvvspa', '0007_auto_20191115_1807'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playerphoto',
            name='owner',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='icon',
            new_name='deliverable',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='icon',
        ),
        migrations.RemoveField(
            model_name='instrument',
            name='url',
        ),
        migrations.RemoveField(
            model_name='order',
            name='url',
        ),
        migrations.RemoveField(
            model_name='player',
            name='url',
        ),
        migrations.AddField(
            model_name='instrument',
            name='thumbnail',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='instrument/images/'),
        ),
        migrations.AddField(
            model_name='order',
            name='music_pkg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tvvspa.Music'),
        ),
        migrations.AddField(
            model_name='player',
            name='thumbnail',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='player/images/'),
        ),
        migrations.AlterField(
            model_name='music',
            name='audio',
            field=models.FileField(blank=True, default=None, null=True, upload_to='music/audio/'),
        ),
        migrations.DeleteModel(
            name='InstrumentPhoto',
        ),
        migrations.DeleteModel(
            name='PlayerPhoto',
        ),
    ]
