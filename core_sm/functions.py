from core_sm.models import Cost
from django.db.models import Avg, Max, Sum, Min
import calendar


def month_day_calculations(day_numbers, year, month, day_sum, day_min, day_max, day_avg):
    for day in day_numbers:
        val_1 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Sum('value'))[
            'value__sum']
        val_2 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Min('value'))[
            'value__min']
        val_3 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Max('value'))[
            'value__max']
        val_4 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day).aggregate(Avg('value'))[
            'value__avg']
        if val_1 and val_2 and val_3 and val_4 is not None:
            val_1 = float(val_1)
            val_2 = float(val_2)
            val_3 = float(val_3)
            val_4 = float(val_4)
            day_sum.append(val_1)
            day_min.append(val_2)
            day_max.append(val_3)
            day_avg.append(val_4)
        else:
            day_sum.append(0)
            day_min.append(0)
            day_max.append(0)
            day_avg.append(0)
    return day_sum, day_min, day_max, day_avg

def month_category_calculation(jedzenie, domowe, kosmetyki_i_chemia, rozrywka, okazyjne, inne):
    for item in Cost.objects.values():
        if item['category'] == 'Jedzenie':
            jedzenie.append(float(item['value']))
        elif item['category'] == 'Domowe':
            domowe.append(float(item['value']))
        elif item['category'] == 'Kosmetyki i Chemia':
            kosmetyki_i_chemia.append(float(item['value']))
        elif item['category'] == 'Rozrywka':
            rozrywka.append(float(item['value']))
        elif item['category'] == 'Okazyjne':
            okazyjne.append(float(item['value']))
        elif item['category'] == 'Inne':
            inne.append(float(item['value']))
    return jedzenie, domowe, kosmetyki_i_chemia, rozrywka, okazyjne, inne

def day_day_calculation(day_data, title, value, category, id):
        for item in day_data.values('title'):
            title.append(item['title'])
        for item in day_data.values('value'):
            value.append(float(item['value']))
        for item in day_data.values('category'):
            category.append(item['category'])
        for item in day_data.values('id'):
            id.append(item['id'])
        return title, value, category, id

def day_category_calculation(day_data, jedzenie, domowe, kosmetyki_i_chemia, rozrywka, okazyjne, inne):
    for item in day_data.values():
        if item['category'] == 'Jedzenie':
            jedzenie.append(float(item['value']))
        elif item['category'] == 'Domowe':
            domowe.append(float(item['value']))
        elif item['category'] == 'Kosmetyki i Chemia':
            kosmetyki_i_chemia.append(float(item['value']))
        elif item['category'] == 'Rozrywka':
            rozrywka.append(float(item['value']))
        elif item['category'] == 'Okazyjne':
            okazyjne.append(float(item['value']))
        elif item['category'] == 'Inne':
            inne.append(float(item['value']))
    return jedzenie, domowe, kosmetyki_i_chemia, rozrywka, okazyjne, inne

def year_month_calculation(Months):
    for item in range(13):
        Months.append(calendar.month_name[item])
    return Months

def year_data_calculation(Months_data, year):
    for item in range(12):
        Months_data.append(Cost.objects.filter(publish__year=year, publish__month=item).aggregate(Sum('value'))['value__sum'])
    return Months_data