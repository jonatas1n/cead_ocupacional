# Generated by Django 3.2.12 on 2022-10-30 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailredirects', '0007_add_autocreate_fields'),
        ('home', '0002_set_homepage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SurveysPage',
        ),
    ]
