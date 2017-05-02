Months = []
    Months_data = []
    Months_url = [str(x).zfill(2) for x in range(13)[1:]]
    year_month_calculation(Months)
    year_data_calculation(Months_data, year, request)
    data = {
        'Miesiące': Months_url,
        'ZŁ': Months_data
    }
    p = Bar(data, values='ZŁ', label='Miesiące', legend=False, plot_width=710, plot_height=350, color='blue')
    script, div = components(p, CDN)
    p_line = Line(data, xlabel='Miesiące', legend=False, plot_width=710, plot_height=350, color='blue')
    script_line, div_line = components(p_line, CDN)
    all_data = zip(Months, Months_data, Months_url)
    year_sum = Cost.objects.filter(publish__year=year, user_id=request.user.id).aggregate(Sum('value'))['value__sum']
    categories = []
    categories_id = []

    for item in Category.objects.filter(user_id=request.user.id).values('title', 'id'):
        categories.append(item['title'])
        categories_id.append(item['id'])

    categories_data = []
    year_categories_calculation(year, categories_id, categories_data, request)
    data1 = {
        'money': [float(x) for x in categories_data],
        'labels': categories
    }
    p1 = Bar(data1, values='money', label='labels', plot_width=710, plot_height=300, legend=False, color='blue')
    script1, div1 = components(p1, CDN)

    year_budget_title = []
    year_budget_spends = []
    year_budget_id = []

    for item in Budget.objects.filter(user_id=request.user.id).values('title', 'id'):
        val = Cost.objects.filter(budget_id=item['id'], publish__year=year, user_id=request.user.id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            year_budget_title.append(item['title'])
            year_budget_spends.append(val)
            year_budget_id.append(item['id'])
        else:
            pass

    year_budget_data = zip(year_budget_title, year_budget_spends, year_budget_id)
    categories_res = zip(categories, categories_data, categories_id)

    another = "/costs/{}/".format(int(year)+1)
    back = "/costs/{}".format(int(year)-1)