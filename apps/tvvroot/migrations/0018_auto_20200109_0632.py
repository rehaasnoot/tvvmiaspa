# Generated by Django 2.2.7 on 2020-01-09 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvvroot', '0017_auto_20200109_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='framespersecond',
            name='fps',
            field=models.CharField(default=None, max_length=25),
        ),
    ]
