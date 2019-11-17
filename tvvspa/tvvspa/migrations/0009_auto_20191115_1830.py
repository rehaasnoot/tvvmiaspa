# Generated by Django 2.2.7 on 2019-11-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tvvspa', '0008_auto_20191115_1819'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='progress',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
