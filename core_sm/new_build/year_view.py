start_date = date_x
end_date = date_y
spends = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user)
stats = []
days = []
days_url = []
for item in spends:
    stats.append(Budget.objects.get(id=item.budget_id).title)

for item in spends.values('publish'):
    days.append(str(item['publish']))
    days_url.append(str(item['publish']).replace('-', '/'))

data = zip(spends, stats, days, days_url)

categories = []
categories_id = []
for item in Category.objects.filter(user=request.user).values('title', 'id'):
    categories.append(item['title'])
    categories_id.append(item['id'])

categories_data = []
comp_categories_calculation(categories_id, categories_data, start_date, end_date, request)
vis_data = {
    'money': [float(x) for x in categories_data],
    'labels': categories
}
p = Bar(vis_data, values='money', label='labels', plot_width=685, plot_height=400, legend=False, color='blue')
script, div = components(p, CDN)

categories_res = zip(categories, categories_data)

data_sum = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Sum('value'))[
    'value__sum']
data_avg = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Avg('value'))[
    'value__avg']
data_min = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Min('value'))[
    'value__min']
data_max = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Max('value'))[
    'value__max']

comp_budget_title = []
comp_budget_spends = []
comp_budget_id = []
for item in Budget.objects.values('title', 'id'):
    val = Cost.objects.filter(budget_id=item['id'], publish__range=(start_date, end_date), user=request.user).aggregate(
        Sum('value'))['value__sum']
    if val is not None:
        comp_budget_title.append(item['title'])
        comp_budget_spends.append(val)
        comp_budget_id.append(item['id'])
    else:
        pass
comp_budget_data = zip(comp_budget_title, comp_budget_spends, comp_budget_id)

if request.method == 'POST':
    form = comp_form(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        return HttpResponseRedirect(reverse('core_sm:stats_comp', args=(cd['date_x'], cd['date_y'])))
else:
    form = comp_form()

budgets_sum = Budget.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Sum('value'))[
    'value__sum']
total_cost_per_budget = sum(comp_budget_spends)

try:
    total_budget = budgets_sum - total_cost_per_budget
except TypeError:
    total_budget = 0
