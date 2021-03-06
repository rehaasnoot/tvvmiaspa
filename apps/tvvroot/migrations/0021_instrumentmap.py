# Generated by Django 2.2.7 on 2020-01-19 18:52

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tvvroot', '0020_auto_20200116_2147'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid1, verbose_name='databasekey')),
                ('classname', models.CharField(max_length=100)),
            ],
        ),
    ]
