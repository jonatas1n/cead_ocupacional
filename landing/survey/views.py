from django.http import HttpRequest, JsonResponse
from survey.models import SurveyPage
from datetime import datetime

months = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

def get_hours(request: HttpRequest):
    hours = []
    minutes = [":00", ":15", ":30", ":45"]
    for hour in list(range(8, 18)):
        for minute in minutes:
            hours.append(str(hour) + minute)

    date = request.GET.get("date")
    apointments = SurveyPage.objects.filter(date=date)
    scheduled = list(map(lambda x: x.hour, apointments))
    hours = [hour for hour in hours if hour not in scheduled]
    
    return JsonResponse(hours, safe=False)

def get_months(request: HttpRequest):
    now = datetime.now()
    actual_month = int(now.strftime("%m")) - 1
    next_months = months[actual_month:]
    
    if len(next_months) < 6:
        more_months = months[:6-len(next_months)]
        next_year = int(now.strftime("%Y")) + 1
        more_months = [f"{month} - {next_year}" for month in more_months]
        next_months += more_months
    
    return JsonResponse(next_months, safe=False)
