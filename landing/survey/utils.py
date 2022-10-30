from survey.models import SurveyPage

def get_disponibility(date):
    hours = []
    minutes = [":00", ":15", ":30", ":45"]
    for hour in list(range(8, 18)):
        for minute in minutes:
            hours.append(str(hour) + minute)

    apointments = SurveyPage.objects.filter(date=date)
    scheduled = list(map(lambda x: x.hour, apointments))
    hours = [hour for hour in hours if hour not in scheduled]
    return hours