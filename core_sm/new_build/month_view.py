def month_stats_detail(request, year, month):
mr = calendar.monthrange(int(year), int(month))
    day_numbers = [str(x).zfill(2) for x in range(mr[1]+1)][1:]
    day_sum = []
    day_min = []
    day_max = []
    day_avg = []
    month_day_calculations(day_numbers, year, month, day_sum, day_min, day_max, day_avg, request)
    day_data = zip(day_numbers, day_sum, day_max, day_min, day_avg)
    data = {
        'Dni': day_numbers,
        'ZŁ': [float(x) for x in day_sum]
    }
    p = Bar(data, values='ZŁ', plot_width=1050, plot_height=300, legend=False, color='blue')
    script, div = components(p, CDN)

    max_month_value = (max(day_max))
    max_month_day = day_numbers[day_max.index(max(day_max))]
    min_month_value = (min(day_min))
    min_month_day = day_numbers[day_min.index(min(day_min))]
    categories = []
    categories_id = []
    for item in Category.objects.filter(user_id=request.user.id).values('title', 'id'):
        categories.append(item['title'])
        categories_id.append(item['id'])

    categories_data = []

    month_category_calculation(year, month, categories_id, categories_data, request)
    data1 = {
        'money': [float(x) for x in categories_data],
        'labels': categories
    }
    p1 = Bar(data1, values='money', label='labels', plot_width=680, plot_height=300, legend=False, color='blue')
    script1, div1 = components(p1, CDN)
    categories_res = zip(categories, categories_data, categories_id)
    sum_cost = Cost.objects.filter(publish__year=year, publish__month=month, user=request.user).aggregate(Sum('value'))
    min_cost = Cost.objects.filter(publish__year=year, publish__month=month, user=request.user).aggregate(Min('value'))
    max_cost = Cost.objects.filter(publish__year=year, publish__month=month, user=request.user).aggregate(Max('value'))
    avg_cost = Cost.objects.filter(publish__year=year, publish__month=month, user=request.user).aggregate(Avg('value'))['value__avg']

    month_budget_title = []
    month_budget_spends = []
    month_budget_id = []
    for item in Budget.objects.values('title', 'id'):
        val = Cost.objects.filter(budget_id=item['id'], publish__year=year, publish__month=month, user=request.user).aggregate(Sum('value'))['value__sum']
        if val is not None:
            month_budget_title.append(item['title'])
            month_budget_spends.append(val)
            month_budget_id.append(item['id'])
        else:
            pass
    month_budget_data = zip(month_budget_title, month_budget_spends, month_budget_id)

    next_month = int(month)+1
    next_year = int(year)

    if next_month > 12:
        next_month = str(1).zfill(2)
        next_year = int(year)+1
    another = "/costs/{}/{}/".format(next_year, next_month)

    back_month = int(month)-1
    back_year = int(year)

    if back_month < 1:
        back_month = 12
        back_year = int(year)-1
    back = "/costs/{}/{}/".format(back_year, back_month)