# Generated by Django 2.2.7 on 2020-01-19 19:34

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

    dependencies = [
        ('tvvroot', '0021_instrumentmap'),
    ]

    operations = [
        migrations.RunPython(install_instrument_classnames),
    ]
