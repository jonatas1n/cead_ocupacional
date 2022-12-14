# Generated by Django 3.2.12 on 2022-11-21 04:44

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('wagtailredirects', '0007_add_autocreate_fields'),
        ('home', '0002_set_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ReturnPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='landingpage',
            name='social_media',
            field=wagtail.core.fields.StreamField([('social_media', wagtail.core.blocks.StructBlock([('service', wagtail.core.blocks.ChoiceBlock(choices=[('instagram', 'Instagram'), ('facebook', 'Facebook'), ('twitter', 'Twitter')], label='Rede Social')), ('link', wagtail.core.blocks.URLBlock(label='Link'))]))], blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='SurveysPage',
        ),
    ]
