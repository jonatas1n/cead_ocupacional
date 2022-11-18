from django.db import migrations
from wagtail.core.models import Page, Site
from home.models import ReturnPage, LandingPage

def create_return_page(apps, schema_editor):
    home_page = LandingPage.objects.first()

    return_page = ReturnPage(title="Sucesso!")

    home_page.add_child(instance=return_page)
    home_page.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("home", "0004_returnpage"),
    ]

    operations = [migrations.RunPython(create_return_page)]
