from django.db import migrations
from home.models import LandingPage
from survey.models import SchedulingPage

def create_schedule_page(apps, schema_editor):
    home_page = LandingPage.objects.first()
    survey_page = SchedulingPage(title='Marque seu exame')
    home_page.add_child(instance=survey_page)
    home_page.save()

class Migration (migrations.Migration):
    dependencies = [
        ('survey', '0003_auto_20221122_0323'),
    ]

    operations = [
        migrations.RunPython(create_schedule_page)
    ]