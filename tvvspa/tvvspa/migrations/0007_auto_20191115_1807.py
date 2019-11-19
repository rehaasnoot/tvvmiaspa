# Generated by Django 2.2.7 on 2019-11-15 18:07

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tvvspa', '0006_auto_20191115_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='music',
            name='audioUrl',
        ),
        migrations.RemoveField(
            model_name='music',
            name='midiUrl',
        ),
        migrations.AddField(
            model_name='music',
            name='audio',
            field=models.FileField(blank=True, default=None, null=True, upload_to='music/midi/'),
        ),
        migrations.AddField(
            model_name='music',
            name='midi',
            field=models.FileField(blank=True, default=None, null=True, upload_to='music/midi/'),
        ),
        migrations.AlterField(
            model_name='playerphoto',
            name='photos',
            field=imagekit.models.fields.ProcessedImageField(upload_to='player/images/'),
        ),
    ]
