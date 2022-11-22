from django.db import migrations
from home.models import LandingPage
from survey.models import SurveyPageIndex

def create_survey_index(apps, schema_editor):
    home_page = LandingPage.objects.first()
    survey_page = SurveyPageIndex(title='Agendamentos')
    home_page.add_child(instance=survey_page)
    home_page.save()

class Migration (migrations.Migration):
    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_survey_index)
    ]