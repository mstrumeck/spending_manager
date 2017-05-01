@login_required
def category_month_stats_detail(request, category_id, year, month):
    category_title = Category.objects.get(id=category_id).title
    mr = calendar.monthrange(int(year), int(month))
    day_numbers = [str(x).zfill(2) for x in range(mr[1] + 1)][1:]
    day_sum = []
    day_min = []
    day_max = []
    day_avg = []
    category_month_day_calculations(day_numbers, year, month, day_sum, day_min, day_max, day_avg, category_id, request)
    day_data = zip(day_numbers, day_sum, day_max, day_min, day_avg)
    data = {
        'Dni': day_numbers,
        'ZŁ': [float(x) for x in day_sum]
    }
    p = Bar(data, values='ZŁ', legend=False, plot_width=1050, plot_height=350, color='blue')
    script, div = components(p, CDN)

    max_month_value = (max(day_max))
    max_month_day = day_numbers[day_max.index(max(day_max))]
    min_month_value = (min(day_min))
    min_month_day = day_numbers[day_min.index(min(day_min))]

    sum_cost = Cost.objects.filter(publish__year=year, publish__month=month,
                                   category_id=category_id, user=request.user).aggregate(Sum('value'))['value__sum']
    min_cost = Cost.objects.filter(publish__year=year, publish__month=month,
                                   category_id=category_id, user=request.user).aggregate(Min('value'))['value__min']
    max_cost = Cost.objects.filter(publish__year=year, publish__month=month,
                                   category_id=category_id, user=request.user).aggregate(Max('value'))['value__max']
    avg_cost = Cost.objects.filter(publish__year=year, publish__month=month,
                                   category_id=category_id, user=request.user).aggregate(Avg('value'))['value__avg']

    month_budget_title = []
    month_budget_spends = []
    month_budget_id = []
    for item in Budget.objects.values('title', 'id'):
        val = \
        Cost.objects.filter(budget_id=item['id'], publish__year=year, publish__month=month, user=request.user).aggregate(Sum('value'))[
            'value__sum']
        if val is not None:
            month_budget_title.append(item['title'])
            month_budget_spends.append(val)
            month_budget_id.append(item['id'])
        else:
            pass

    budgets = []
    budgets_id = []
    budgets_data = []

    for item in Budget.objects.filter(user=request.user).values('title', 'id'):
        budgets.append(item['title'])
        budgets_id.append(item['id'])

    for item in budgets_id:
        val = Cost.objects.filter(publish__year=year, publish__month=month, category_id=category_id,
        budget_id=item, user=request.user).aggregate(Sum('value'))['value__sum']
        if val is not None:
            budgets_data.append(val)
        else:
            budgets_data.append(0)
    data1 = {
        'money': [float(x) for x in budgets_data],
        'labels': budgets
    }
    p1 = Bar(data1, values='money', label='labels', plot_width=810, plot_height=300, legend=False, color='blue')
    script1, div1 = components(p1, CDN)

    month_budget_data = zip(month_budget_title, month_budget_spends, month_budget_id)

    next_month = int(month) + 1
    next_year = int(year)

    if next_month > 12:
        next_month = str(1).zfill(2)
        next_year = int(year) + 1
    another = "/category/{}/{}/{}/".format(category_id, next_year, next_month)

    back_month = int(month) - 1
    back_year = int(year)

    if back_month < 1:
        back_month = 12
        back_year = int(year) - 1
    back = "/category/{}/{}/{}/".format(category_id, back_year, back_month)

    return render(request, 'core_sm/costs/category/category_month_detail.html', {'year': year,
                                                                                 'category_id': category_id,
                                                                                 'month': month,
                                                                                 'sum_cost': sum_cost,
                                                                                 'min_cost': min_cost,
                                                                                 'max_cost': max_cost,
                                                                                 'avg_cost': avg_cost,
                                                                                 'day_numbers': day_numbers,
                                                                                 'day_data': day_data,
                                                                                 'max_month_value': max_month_value,
                                                                                 'max_month_day': max_month_day,
                                                                                 'min_month_value': min_month_value,
                                                                                 'min_month_day': min_month_day,
                                                                                 'script': mark_safe(script),
                                                                                 'div': mark_safe(div),
                                                                                 'script1': mark_safe(script1),
                                                                                 'div1': mark_safe(div1),
                                                                                 'month_budget_data': month_budget_data,
                                                                                 'category_title': category_title,
                                                                                 'another': another,
                                                                                 'back': back})