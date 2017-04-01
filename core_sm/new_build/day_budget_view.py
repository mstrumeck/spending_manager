def budget_day_stats_detail(request, id, year, month, day):
    budget_owner = User.objects.get(id=Budget.objects.get(id=id).user_id).username
    budget_day_title = Budget.objects.get(id=id).title
    total = Cost.objects.filter(budget_id=id, user=request.user).aggregate(Sum('value'))['value__sum']
    budget = Budget.objects.get(id=id).value

    try:
        total_budget = budget - total
    except TypeError:
        total_budget = 0

    day_data = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day, budget_id=id, user=request.user)
    title = []
    value = []
    category = []
    product_id = []
    budget_day_calculation(day_data, title, value, category, product_id)
    all_data = zip(title, value, category, product_id)

    try:
        day_max = [title[value.index(max(value))], max(value), category[value.index(max(value))]]
    except(ValueError, TypeError):
        day_max = 0
    try:
        day_min = [title[value.index(min(value))], min(value), category[value.index(min(value))]]
    except(ValueError, TypeError):
        day_min = 0

    day_sum = day_data.aggregate(Sum('value'))
    day_avg = day_data.aggregate(Avg('value'))['value__avg']
    categories = []
    categories_data = []

    for item in Category.objects.values('title'):
        categories.append(item['title'])

    day_category_calculation(year, month, day, categories, categories_data, request)
    data = {
                'money': [float(x) for x in categories_data],
                'labels': categories
            }

    p = Bar(data, values='money', label='labels', plot_width=760, plot_height=300, legend=False, color='blue')
    script, div = components(p, CDN)

    categories_res = zip(categories, categories_data)
    return render(request, 'core_sm/costs/budget/budget_day_detail.html', {'year': year,
                                                                           'month': month,
                                                                           'day': day,
                                                                           'id': id,
                                                                           'day_data': day_data,
                                                                           'all_data': all_data,
                                                                           'day_sum': day_sum['value__sum'],
                                                                           'day_avg': day_avg,
                                                                           'script': mark_safe(script),
                                                                           'div': mark_safe(div),
                                                                           'day_max': day_max,
                                                                           'day_min': day_min,
                                                                           'total_budget': total_budget,
                                                                           'categories_res': categories_res,
                                                                           'budget_day_title': budget_day_title,
                                                                           'budget_owner': budget_owner})