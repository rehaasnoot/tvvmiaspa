# Generated by Django 2.2.7 on 2020-01-23 00:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields
import uuid


# Functions from the following migrations need manual copying.
# Move them and any dependencies into this file, then update the
# RunPython operations to refer to the local versions:
# apps.tvvroot.migrations.0022_auto_20200119_1934
# apps.tvvroot.migrations.0026_instrumentmap_limbs

from django.db import migrations

def install_instrument_classnames(apps, schema_editor):
    ## Install TVV MIA class names
    INSTRUMENT_CLASSNAMES = ['Bass', 'HofnerBass', 'UprightBass','Guitar', "LeadGuitar", 'RhythmGuitar',
                             'AccousticGuitar', 'ClassicalGuitar', 'FolkGuitar', 'Piano', 'HammondB3', 'Trombone', 
                             'Trumpet', 'AltoSax', 'DrumKit', 'ElectroniDrumKit', 'Violin', 'Viola', 'Cello', 'Fiddle', 
                             'Vibrophone', 'Marimba']
                       
    IM = apps.get_model('tvvroot', 'InstrumentMap')
    for cn in INSTRUMENT_CLASSNAMES:
        m = IM.objects.find(classname=cn)
        if None == m:
            im = IM.objects.create()
            im.classname = cn
            im.save()

class Migration(migrations.Migration):

    replaces = [('tvvroot', '0001_initial'), ('tvvroot', '0002_video'), ('tvvroot', '0003_blender'), ('tvvroot', '0004_auto_20191121_1519'), ('tvvroot', '0005_auto_20191121_1543'), ('tvvroot', '0006_auto_20191121_1545'), ('tvvroot', '0007_auto_20191121_2327'), ('tvvroot', '0008_auto_20191122_0332'), ('tvvroot', '0009_video_video_url'), ('tvvroot', '0010_auto_20191128_1456'), ('tvvroot', '0011_auto_20191202_0714'), ('tvvroot', '0012_auto_20191205_2116'), ('tvvroot', '0013_order_midi_track'), ('tvvroot', '0014_order_frames_per_second'), ('tvvroot', '0015_framespersecond'), ('tvvroot', '0016_auto_20200109_0614'), ('tvvroot', '0017_auto_20200109_0620'), ('tvvroot', '0018_auto_20200109_0632'), ('tvvroot', '0019_auto_20200116_2147'), ('tvvroot', '0020_auto_20200116_2147'), ('tvvroot', '0021_instrumentmap'), ('tvvroot', '0022_auto_20200119_1934'), ('tvvroot', '0023_instrument_classname'), ('tvvroot', '0024_auto_20200120_1250'), ('tvvroot', '0025_auto_20200120_1251'), ('tvvroot', '0026_instrumentmap_limbs')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=256)),
                ('blend_file', models.FileField(blank=True, default=None, null=True, upload_to='instrument/blend/')),
                ('thumbnail_orig', models.ImageField(blank=True, default=None, null=True, upload_to='instrument/images/')),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('title', models.CharField(max_length=100)),
                ('midi', models.FileField(blank=True, default=None, null=True, upload_to='music/midi/')),
                ('audio', models.FileField(blank=True, default=None, null=True, upload_to='music/audio/')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=256)),
                ('blend_file', models.FileField(blank=True, default=None, null=True, upload_to='player/blend/')),
                ('thumbnail_orig', models.ImageField(blank=True, default=None, null=True, upload_to='player/images/')),
            ],
        ),
        migrations.CreateModel(
            name='UserPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photos', imagekit.models.fields.ProcessedImageField(upload_to='user/images/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('description', models.CharField(blank=True, default=None, max_length=512, null=True)),
                ('is_complete', models.BooleanField(default=False)),
                ('in_progress', models.BooleanField(default=False)),
                ('progress', models.PositiveSmallIntegerField(default=0)),
                ('deliverable', models.URLField(blank=True, default=None, null=True)),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvvroot.Instrument')),
                ('music_pkg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tvvroot.Music')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvvroot.Player')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('end_frame', models.PositiveSmallIntegerField(default=250)),
                ('start_frame', models.PositiveSmallIntegerField(default=0)),
                ('midi_track', models.PositiveSmallIntegerField(default=1)),
                ('frames_per_second', models.PositiveSmallIntegerField(default=24)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('title', models.CharField(max_length=100)),
                ('video_uri', models.FileField(blank=True, default=None, null=True, upload_to='music/video/')),
                ('codec', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('video_url', models.URLField(blank=True, default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('status', models.CharField(choices=[('PENDING', 'Blender agent pending'), ('REQUESTED', 'Blender agent requested'), ('STARTING', 'Blender agent starting'), ('RUNNING', 'Blender agent running'), ('ENDING', 'Blender agent ending'), ('ENDED', 'Blender agent ending')], default='PENDING', max_length=32, verbose_name='status')),
                ('progress', models.PositiveSmallIntegerField(default=0)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvvroot.Order')),
                ('frame_end', models.PositiveIntegerField(default=250)),
                ('frame_start', models.PositiveIntegerField(default=1)),
                ('pid', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='FramesPerSecond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fps', models.CharField(default=None, max_length=25)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='frames_per_second',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tvvroot.FramesPerSecond'),
        ),
        migrations.RenameField(
            model_name='order',
            old_name='midi_track',
            new_name='midi_track_left_hand',
        ),
        migrations.AddField(
            model_name='order',
            name='midi_track_left_foot',
            field=models.PositiveSmallIntegerField(default=3),
        ),
        migrations.AddField(
            model_name='order',
            name='midi_track_right_foot',
            field=models.PositiveSmallIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='order',
            name='midi_track_right_hand',
            field=models.PositiveSmallIntegerField(default=2),
        ),
        migrations.CreateModel(
            name='InstrumentMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('classname', models.CharField(max_length=100)),
            ],
        ),
        migrations.RunPython(
            #code=apps.tvvroot.migrations.0022_auto_20200119_1934.install_instrument_classnames,
            code=install_instrument_classnames
        ),
        migrations.AddField(
            model_name='instrument',
            name='classname',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='tvvroot.InstrumentMap'),
        ),
        migrations.AddField(
            model_name='instrumentmap',
            name='limbs',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
#        migrations.RunPython(
#            code=apps.tvvroot.migrations.0026_instrumentmap_limbs.install_instrument_classnames,
#        ),
    ]