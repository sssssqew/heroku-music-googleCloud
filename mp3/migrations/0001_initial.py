# Generated by Django 2.0 on 2020-08-22 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.TextField()),
                ('album', models.TextField()),
                ('title', models.TextField()),
                ('artist', models.TextField()),
                ('genre', models.TextField()),
                ('release', models.TextField()),
                ('lyrics', models.TextField()),
                ('duration', models.TextField()),
                ('cloudSrc', models.TextField()),
            ],
        ),
    ]