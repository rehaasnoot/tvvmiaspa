# Generated by Django 2.2.7 on 2019-11-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvvroot', '0004_auto_20191121_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='in_progress',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]