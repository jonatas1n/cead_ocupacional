from django.db import migrations
import wagtail.core.fields
from wagtail.core.models import Page

from home.models import LandingPage
from survey.models import SurveyPageIndex

def create_survey_index_page(apps, schema_editor):
    home_page = LandingPage.objects.all()[0]

    survey_index = SurveyPageIndex(title="Agendamentos", slug="survey")

    home_page.add_child(instance=survey_index)
    home_page.save()

class Migration(migrations.Migration):
    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_survey_index_page),
    ]
