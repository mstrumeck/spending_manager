from core_sm.models import Cost, Budget, Category
from django.db.models import Avg, Max, Sum, Min
import calendar
import datetime


def comp_categories_calculation(categories, categories_data, start_date, end_date):
    for item in categories:
        val = Cost.objects.filter(publish__range=(start_date, end_date), category_id=
        Category.objects.get(title='{}'.format(item)).id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            categories_data.append(val)
        else:
            categories_data.append(0)
    return categories_data


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
            day_sum.append(val_1)
            day_min.append(val_2)
            day_max.append(val_3)
            day_avg.append("%.2f" % val_4)
        else:
            day_sum.append(0)
            day_min.append(0)
            day_max.append(0)
            day_avg.append(0)
    return day_sum, day_min, day_max, day_avg


def month_category_calculation(year, month, categories, categories_data):
    for item in categories:
        val = Cost.objects.filter(publish__year=year, publish__month=month, category_id=
        Category.objects.get(title='{}'.format(item)).id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            categories_data.append(val)
        else:
            categories_data.append(0)


def day_day_calculation(day_data, title, value, category, day_id, budget_id):
        for item in day_data.values('title', 'value', 'category_id', 'id', 'budget_id'):
            title.append(item['title'])
            value.append(float(item['value']))
            category.append(Category.objects.get(id=item['category_id']).title)
            day_id.append(item['id'])
            budget_id.append(Budget.objects.get(id=item['budget_id']).title)
        return title, value, category, day_id, budget_id


def day_category_calculation(year, month, day, categories, categories_data):
    for data in categories:
        val = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day, category_id=
        Category.objects.get(title='{}'.format(data)).id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            categories_data.append(val)
        else:
            categories_data.append(0)
    return categories_data


def year_month_calculation(Months):
    for item in range(13)[1:]:
        Months.append(calendar.month_name[item])
    return Months


def year_data_calculation(Months_data, year):
    for item in range(13)[1:]:
        val = Cost.objects.filter(publish__year=year, publish__month=item).aggregate(Sum('value'))['value__sum']
        if val is not None:
            Months_data.append(float(val))
        else:
            Months_data.append(0)
    return Months_data


def year_categories_calculation(year, categories, categories_data):
    for data in categories:
        val = Cost.objects.filter(publish__year=year, category_id=
        Category.objects.get(title='{}'.format(data)).id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            categories_data.append(val)
        else:
            categories_data.append(0)
    return categories_data


def budget_categories_calculation(id, categories, categories_data):
    for data in categories:
        val = Cost.objects.filter(budget_id=id, category_id=Category.objects.get(title='{}'.format(data)).id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            categories_data.append(val)
        else:
            categories_data.append(0)
    return categories_data


def year_budget_calculation(Months_data, year, id):
    for item in range(13)[1:]:
        val = Cost.objects.filter(publish__year=year, publish__month=item, budget_id=id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            Months_data.append(float(val))
        else:
            Months_data.append(0)
    return Months_data


def year_budget_categories_calculation(year, categories, categories_data, id):
    for data in categories:
        val = Cost.objects.filter(publish__year=year, category_id=
        Category.objects.get(title='{}'.format(data)).id, budget_id=id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            categories_data.append(val)
        else:
            categories_data.append(0)
    return categories_data


def budget_month_day_calculations(day_numbers, year, month, day_sum, day_min, day_max, day_avg, id):
    for day in day_numbers:
        val_1 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    budget_id=id).aggregate(Sum('value'))['value__sum']
        val_2 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    budget_id=id).aggregate(Min('value'))['value__min']
        val_3 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    budget_id=id).aggregate(Max('value'))['value__max']
        val_4 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    budget_id=id).aggregate(Avg('value'))['value__avg']
        if val_1 and val_2 and val_3 and val_4 is not None:
            day_sum.append(val_1)
            day_min.append(val_2)
            day_max.append(val_3)
            day_avg.append("%.2f" % val_4)
        else:
            day_sum.append(0)
            day_min.append(0)
            day_max.append(0)
            day_avg.append(0)
    return day_sum, day_min, day_max, day_avg


def budget_month_category_calculation(year, month, id, categories, categories_data):
    for item in categories:
        val = Cost.objects.filter(publish__year=year, publish__month=month, category_id=
        Category.objects.get(title='{}'.format(item)).id, budget_id=id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            categories_data.append(val)
        else:
            categories_data.append(0)


def budget_day_calculation(day_data, title, value, category, product_id):
    for item in day_data.values('title'):
        title.append(item['title'])
    for item in day_data.values('value'):
        value.append(float(item['value']))
    for item in day_data.values('category_id'):
        category.append(Category.objects.get(id=item['category_id']).title)
    for item in day_data.values('id'):
        product_id.append(item['id'])
    return title, value, category, product_id


def category_year_data_calculation(Months_data, year, category_id):
    for item in range(13)[1:]:
        val = Cost.objects.filter(publish__year=year, publish__month=item, category_id=category_id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            Months_data.append(float(val))
        else:
            Months_data.append(0)
    return Months_data


def category_month_day_calculations(day_numbers, year, month, day_sum, day_min, day_max, day_avg, category_id):
    for day in day_numbers:
        val_1 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    category_id=category_id).aggregate(Sum('value'))['value__sum']
        val_2 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    category_id=category_id).aggregate(Min('value'))['value__min']
        val_3 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    category_id=category_id).aggregate(Max('value'))['value__max']
        val_4 = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day,
                                    category_id=category_id).aggregate(Avg('value'))['value__avg']
        if val_1 and val_2 and val_3 and val_4 is not None:
            day_sum.append(val_1)
            day_min.append(val_2)
            day_max.append(val_3)
            day_avg.append("%.2f" % val_4)
        else:
            day_sum.append(0)
            day_min.append(0)
            day_max.append(0)
            day_avg.append(0)
    return day_sum, day_min, day_max, day_avg


def category_day_day_calculation(day_data, title, value, day_id, budget_id):
    for item in day_data.values('title', 'value', 'id', 'budget_id'):
        title.append(item['title'])
        value.append(float(item['value']))
        day_id.append(item['id'])
        budget_id.append(Budget.objects.get(id=item['budget_id']).title)
    return title, value, day_id, budget_id
