from django.http import HttpRequest, JsonResponse
from datetime import datetime, timedelta
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from survey.utils import get_disponibility

months = [None, 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
week_days = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

def get_hours(request: HttpRequest):
    date = request.GET.get("date")
    print(date)
    hours = get_disponibility(date)
    
    return JsonResponse(hours, safe=False)

def get_months(request: HttpRequest):
    month_index = request.GET.get('month_index', 0)
    month_index = int(month_index)
    if month_index > 6:
        return

    month_data = {}
    now = datetime.now() + relativedelta(months=month_index)
    now = now.replace(day=1)

    title = months[int(now.strftime('%m'))]
    if int(now.strftime('%m')) - month_index < 0:
        title += now.strftime(f" - %Y")
    month_data['title'] = title

    total_days = monthrange(now.year, now.month)[1]
    week_day_num = int(now.strftime("%w"))

    month_data['days'] = []
    
    total = 42 - total_days - week_day_num
    for i in range(week_day_num * -1, total_days + total):
        day = now + timedelta(days=i)
        week_day = int(day.strftime('%w'))
        
        is_valid = day > datetime.now()

        disponibility = get_disponibility(day.strftime("%Y-%m-%d"))
        is_valid = is_valid and len(disponibility) > 0

        data = {
            'day_num': day.strftime('%d'),
            'week_day': week_days[week_day].lower()[:3],
            'url_parameter': day.strftime("%Y-%m-%d"),
            'status': is_valid,
            'this_month': 0 < i < total_days,
            'date': day.strftime('%Y-%m-%d'),
        }

        month_data['days'].append(data)
    
    month_data['days_after_sunday'] = week_day_num

    return JsonResponse(month_data)
