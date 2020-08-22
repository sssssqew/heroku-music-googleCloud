# Generated by Django 2.0 on 2020-08-22 13:13

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
                ('cover', models.CharField(max_length=500, null=True)),
                ('album', models.CharField(max_length=300, null=True)),
                ('title', models.CharField(max_length=300, null=True)),
                ('artist', models.CharField(max_length=300, null=True)),
                ('genre', models.CharField(max_length=300, null=True)),
                ('release', models.CharField(max_length=300, null=True)),
                ('lyrics', models.CharField(max_length=300, null=True)),
                ('duration', models.CharField(max_length=300, null=True)),
                ('cloudSrc', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]
