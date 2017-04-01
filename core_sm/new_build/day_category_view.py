def category_day_stats_detail(request, year, month, day, category_id):
    category_title = Category.objects.get(id=category_id).title
    day_data = Cost.objects.filter(user=request.user, publish__year=year, publish__month=month, publish__day=day, category_id=category_id)
    title = []
    value = []
    day_id = []
    budget_id = []
    category_day_day_calculation(day_data, title, value, day_id, budget_id)
    all_data = zip(day_data, budget_id)

    try:
        day_max = [title[value.index(max(value))], max(value), budget_id[value.index(max(value))]]
    except(ValueError, TypeError):
        day_max = 0

    try:
        day_min = [title[value.index(min(value))], min(value), budget_id[value.index(min(value))]]
    except(ValueError, TypeError):
        day_min = 0

    day_sum = day_data.aggregate(Sum('value'))['value__sum']
    day_avg = day_data.aggregate(Avg('value'))['value__avg']

    day_budget_title = []
    day_budget_spends = []
    day_budget_id = []
    for item in Budget.objects.values('title', 'id'):
        val = Cost.objects.filter(budget_id=item['id'], publish__year=year, user=request.user,
                                  publish__month=month, publish__day=day, category_id=category_id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            day_budget_title.append(item['title'])
            day_budget_spends.append(val)
            day_budget_id.append(item['id'])
        else:
            pass

    day_budget_data = zip(day_budget_title, day_budget_spends, day_budget_id)

    data = {
        'money': [float(x) for x in day_budget_spends],
        'labels': day_budget_title
    }
    p1 = Bar(data, values='money', label='labels', plot_width=800, plot_height=300, legend=False, color='blue')
    script, div = components(p1, CDN)
    return render(request, 'core_sm/costs/category/category_day_detail.html', {'year': year,
                                                                               'month': month,
                                                                               'category_id': category_id,
                                                                               'day': day,
                                                                               'day_data': day_data,
                                                                               'all_data': all_data,
                                                                               'day_sum': day_sum,
                                                                               'day_avg': day_avg,
                                                                               'day_max': day_max,
                                                                               'day_min': day_min,
                                                                               'day_budget_data': day_budget_data,
                                                                               'category_title': category_title,
                                                                               'script': mark_safe(script),
                                                                               'div': mark_safe(div)})