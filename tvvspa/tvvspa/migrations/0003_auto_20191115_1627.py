# Generated by Django 2.2.7 on 2019-11-15 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvvspa', '0002_auto_20191115_1611'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='uri',
        ),
        migrations.AddField(
            model_name='instrument',
            name='icon',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='music',
            name='icon',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='icon',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='icon',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='instrument',
            name='url',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='music',
            name='midiUrl',
            field=models.URLField(blank=True, default=None, null=True),
        ),
    ]
