# Generated by Django 2.0 on 2020-08-21 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mp3', '0010_audiofile_cloudsrc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofile',
            name='encodedBy',
        ),
    ]