# Generated by Django 3.2.12 on 2022-10-30 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_create_index'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveypage',
            name='survey',
        ),
    ]
