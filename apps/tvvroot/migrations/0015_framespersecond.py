# Generated by Django 2.2.7 on 2020-01-09 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvvroot', '0014_order_frames_per_second'),
    ]

    operations = [
        migrations.CreateModel(
            name='FramesPerSecond',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fps', models.SmallIntegerField(default=None)),
            ],
        ),
    ]
