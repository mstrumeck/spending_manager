def day_stats_detail(request, year, month, day):
    day_data = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day, user_id=request.user.id)
    title = []
    value = []
    category = []
    day_id = []
    budget_id = []
    day_day_calculation(day_data, title, value, category, day_id, budget_id)
    all_data = zip(day_data, budget_id)

    try:
        day_max = [title[value.index(max(value))], max(value), category[value.index(max(value))],
                   budget_id[value.index(max(value))]]
    except(ValueError, TypeError):
        day_max = 0

    try:
        day_min = [title[value.index(min(value))], min(value), category[value.index(min(value))],
                   budget_id[value.index(min(value))]]
    except(ValueError, TypeError):
        day_min = 0

    day_sum = day_data.aggregate(Sum('value'))
    day_avg = day_data.aggregate(Avg('value'))['value__avg']
    categories = []
    categories_id = []

    for item in Category.objects.filter(user_id=request.user.id).values('title', 'id'):
        categories.append(item['title'])
        categories_id.append(item['id'])

    categories_data = []
    day_category_calculation(year, month, day, categories_id, categories_data, request)
    data = {
        'money': [float(x) for x in categories_data],
        'labels': categories
    }
    p = Bar(data, values='money', label='labels', plot_width=600, plot_height=300, legend=False, color='blue')
    script, div = components(p, CDN)

    categories_res = zip(categories, categories_data, categories_id)

    day_budget_title = []
    day_budget_spends = []
    day_budget_id = []

    for item in Budget.objects.filter(user_id=request.user.id).values('title', 'id'):
        val = Cost.objects.filter(budget_id=item['id'], publish__year=year, publish__month=month, publish__day=day, user_id=request.user.id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            day_budget_title.append(item['title'])
            day_budget_spends.append(val)
            day_budget_id.append(item['id'])
        else:
            pass
    day_budget_data = zip(day_budget_title, day_budget_spends, day_budget_id)

    mr = calendar.monthrange(int(year), int(month))
    next_year = int(year)
    next_month = int(month)
    next_day = int(day) + 1
    if next_day > mr[1]:
        next_day = str(1).zfill(2)
        next_month = str(next_month + 1).zfill(2)
    if int(next_month) > 12:
        next_month = str(1).zfill(2)
        next_year += 1
    another = "/costs/{}/{}/{}/".format(next_year, next_month, next_day)

    back_year = int(year)
    back_year = int(year)
    back_month = int(month)
    back_day = int(day)-1
    if back_day < 1:
        back_day = calendar.monthrange(int(year), int(month)-1)[1]
        back_month = "%.2f" % (back_month - 1)
    back = "/costs/{}/{}/{}/".format(back_year, back_month, back_day)
    return render(request, 'core_sm/costs/day_stats_detail.html', {'year': year,
                                                                   'month': month,
                                                                   'day': day,
                                                                   'day_data': day_data,
                                                                   'all_data': all_data,
                                                                   'day_sum': day_sum['value__sum'],
                                                                   'day_avg': day_avg,
                                                                   'script': mark_safe(script),
                                                                   'div': mark_safe(div),
                                                                   'day_max': day_max,
                                                                   'day_min': day_min,
                                                                   'categories_res': categories_res,
                                                                   'day_budget_data': day_budget_data,
                                                                   'another': another,
                                                                   'back': back,
                                                                   'categories_id': categories_id})