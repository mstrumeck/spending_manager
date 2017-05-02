from core_sm.classes import DayView, DayViewCategory, DayViewBudget, MonthView, MonthViewCategory, MonthViewBudget, \
    YearView
from django.shortcuts import HttpResponseRedirect
from .models import Cost, Budget, Category
from django.db.models import Avg, Max, Min, Sum
from .forms import DataGenerateForm, DataAddForm, MultiaddGenerateForm, comp_form, BudgetForm, \
    CategoryForm
from django.core.urlresolvers import reverse
import datetime
from bokeh.embed import components
from django.utils.safestring import mark_safe
from bokeh.resources import CDN
from bokeh.charts import Bar, Line
import calendar
from django.forms import modelformset_factory
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from core_sm.functions import month_day_calculations, month_category_calculation, \
    day_day_calculation, day_category_calculation, year_data_calculation, year_month_calculation, \
    year_categories_calculation, comp_categories_calculation, budget_categories_calculation, year_budget_calculation, \
    year_budget_categories_calculation, budget_month_day_calculations, budget_month_category_calculation, \
    budget_day_calculation, category_year_data_calculation, category_month_day_calculations, category_day_day_calculation


@login_required
def category_delete(request, category_id):
    title = Category.objects.get(id=category_id).title
    Category.objects.get(id=category_id).delete()
    return render(request, 'core_sm/costs/category/category_delete.html', {'title': title})


@login_required
def category_edit(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm(instance=category)
    return render(request, 'core_sm/costs/category/category_edit.html', {'form': form,
                                                                         'category': category})


@login_required
def category_setup(request):
    add = False
    info_total = []
    info_url = []
    info = Category.objects.filter(user_id=User.objects.get(username=request.user).id)
    for item in info:
        info_total.append(Cost.objects.filter(category_id=item.id, user=request.user).aggregate(Sum('value'))['value__sum'])
        info_url.append(str(item.publish).replace('-', '/'))

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            add = True
            f = form.save(commit=False)
            f.user = request.user
            f.save()
    else:
        form = CategoryForm

    data = zip(info, info_total, info_url)

    return render(request, 'core_sm/costs/category/category_setup.html', {'data': data,
                                                                          'form': form,
                                                                          'add': add})


@login_required
def category_day_stats_detail(request, category_id, year, month, day):
    dd = DayViewCategory(year, month, day, category_id, request)
    dd.day_max_min()
    dd.budget_title_calculation()
    dd.day_calculation()
    return render(request, 'core_sm/costs/category/category_day_detail.html', {'year': dd.year,
                                                                     'month': dd.month,
                                                                     'day': dd.day,
                                                                     'title': dd.category_title,
                                                                     'day_data': dd.day_data,
                                                                     'budget_zip': dd.budget_zip,
                                                                     'category_budget_zip': dd.category_budget_zip,
                                                                     'day_sum': dd.day_sum,
                                                                     'day_max': dd.day_max,
                                                                     'day_min': dd.day_min,
                                                                     'day_avg': dd.day_avg,})


@login_required
def category_month_stats_detail(request, category_id, year, month):
    dd = MonthViewCategory(request, year, month, category_id)
    dd.month_calculation()
    dd.month_category_calculation()
    dd.month_budget_calculation()
    dd.month_figures_days()

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

    return render(request, 'core_sm/costs/category/category_month_detail.html', {'year': dd.year,
                                                                     'month': dd.month,
                                                                     'day_data': dd.day_data,
                                                                     'div': mark_safe(dd.div),
                                                                     'script': mark_safe(dd.script),
                                                                     'budget_zip': dd.budget_zip,
                                                                     'month_sum': dd.month_sum,
                                                                     'month_avg': dd.month_avg,
                                                                     'category_title': dd.category_title,
                                                                     'back': back,
                                                                     'another': another})

@login_required
def category_year_stats_detail(request, category_id, year):
    category_title = Category.objects.get(id=category_id).title
    Months = []
    Months_data = []
    Months_url = [str(x).zfill(2) for x in range(13)[1:]]
    year_month_calculation(Months)
    category_year_data_calculation(Months_data, year, category_id, request)
    data = {
        'Miesiące': Months_url,
        'ZŁ': Months_data
    }
    p = Bar(data, values='ZŁ', label='Miesiące', legend=False, plot_width=910, plot_height=350, color='blue')
    script, div = components(p, CDN)
    all_data = zip(Months, Months_data, Months_url)
    year_sum = Cost.objects.filter(publish__year=year, category_id=category_id, user=request.user).aggregate(Sum('value'))['value__sum']

    year_budget_title = []
    year_budget_spends = []
    year_budget_id = []

    for item in Budget.objects.filter(user=request.user).values('title', 'id'):
        val = Cost.objects.filter(budget_id=item['id'], publish__year=year, category_id=category_id, user=request.user).aggregate(Sum('value'))['value__sum']
        if val is not None:
            year_budget_title.append(item['title'])
            year_budget_spends.append(val)
            year_budget_id.append(item['id'])
        else:
            pass

    year_budget_data = zip(year_budget_title, year_budget_spends, year_budget_id)

    budgets = []
    budgets_id = []
    budgets_data = []

    for item in Budget.objects.filter(user=request.user).values('title', 'id'):
        budgets.append(item['title'])
        budgets_id.append(item['id'])

    for item in budgets_id:
        val = Cost.objects.filter(publish__year=year,
                                  category_id=category_id,
                                  user=request.user,
                                  budget_id=item).aggregate(Sum('value'))['value__sum']
        if val is not None:
            budgets_data.append(val)
        else:
            budgets_data.append(0)

    data1 = {
        'money': [float(x) for x in budgets_data],
        'labels': budgets
    }
    p1 = Bar(data1, values='money', label='labels', legend=False, plot_width=810, plot_height=350, color='blue')
    script1, div1 = components(p1, CDN)

    another = "/category/{}/{}/".format(category_id, (int(year) + 1))
    back = "/category/{}/{}/".format(category_id, (int(year) + 1))

    return render(request, 'core_sm/costs/category/category_year_detail.html', {'category_title': category_title,
                                                                                'category_id': category_id,
                                                                                'year': year,
                                                                                'script': mark_safe(script),
                                                                                'div': mark_safe(div),
                                                                                'all_data': all_data,
                                                                                'year_sum': year_sum,
                                                                                'year_budget_data': year_budget_data,
                                                                                'another': another,
                                                                                'back': back,
                                                                                'script1': mark_safe(script1),
                                                                                'div1': mark_safe(div1)})

@login_required
def category_detail(request, category_id):
    category_title = Category.objects.get(id=category_id).title
    spends = Cost.objects.filter(category_id=category_id, user=request.user)
    stats = []
    days = []
    days_url = []
    for item in spends:
        stats.append(Budget.objects.get(id=item.budget_id).title)

    for item in spends.values('publish'):
        days.append(str(item['publish']))
        days_url.append(str(item['publish']).replace('-', '/'))

    data = zip(spends, stats, days, days_url)

    data_sum = Cost.objects.filter(category_id=category_id, user=request.user).aggregate(Sum('value'))['value__sum']
    data_avg = Cost.objects.filter(category_id=category_id, user=request.user).aggregate(Avg('value'))['value__avg']
    data_min = Cost.objects.filter(category_id=category_id, user=request.user).aggregate(Min('value'))['value__min']
    data_max = Cost.objects.filter(category_id=category_id, user=request.user).aggregate(Max('value'))['value__max']

    category_budget_title = []
    category_budget_spends = []
    category_budget_id = []

    for item in Budget.objects.values('title', 'id'):
        val = Cost.objects.filter(budget_id=item['id'], category_id=category_id, user=request.user).aggregate(Sum('value'))[
            'value__sum']
        if val is not None:
            category_budget_title.append(item['title'])
            category_budget_spends.append(val)
            category_budget_id.append(item['id'])
        else:
            pass

    budgets = []
    budgets_id = []
    budgets_data = []

    for item in Budget.objects.filter(user=request.user).values('title', 'id'):
        budgets.append(item['title'])
        budgets_id.append(item['id'])

    for item in budgets:
        val = Cost.objects.filter(category_id=category_id, user=request.user, budget_id=Budget.objects.get(title='{}'.format(item)).id).aggregate(Sum('value'))['value__sum']
        if val is not None:
            budgets_data.append(val)
        else:
            budgets_data.append(0)

    table_data = {
        'money': [float(x) for x in budgets_data],
        'labels': budgets
    }
    p1 = Bar(table_data, values='money', label='labels', legend=False, plot_width=810, plot_height=350, color='blue')
    script, div = components(p1, CDN)

    category_budget_data = zip(category_budget_title, category_budget_spends, category_budget_id)

    return render(request, 'core_sm/costs/category/category_detail.html', {'data': data,
                                                                           'data_sum': data_sum,
                                                                           'data_avg': data_avg,
                                                                           'data_min': data_min,
                                                                           'data_max': data_max,
                                                                           'category_title': category_title,
                                                                           'category_budget_data': category_budget_data,
                                                                           'script': mark_safe(script),
                                                                           'div': mark_safe(div)})


def budget_item_delete(request, id):
    message = '{} został pomyslnie usunięty'.format(Cost.objects.get(id=id).title)
    Cost.objects.get(id=id).delete()
    return render(request, 'core_sm/costs/budget/budget_item_delete.html', {'message': message})


def budget_delete(request, budget_id):
    title = Budget.objects.get(id=budget_id).title
    Budget.objects.get(id=budget_id).delete()
    return render(request, 'core_sm/costs/budget/budget_delete.html', {'title': title})


def budget_edit(request, id):
    budget = Budget.objects.get(id=id)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'core_sm/costs/budget/budget_edit.html', {'budget': budget,
                                                                     'form': form})


@login_required
def budget_day_stats_detail(request, budget_id, year, month, day):
    dd = DayViewBudget(year, month, day, budget_id, request)
    dd.category_title_calculation()
    dd.day_calculation()
    dd.day_figure()
    return render(request, 'core_sm/costs/budget/budget_day_detail.html', {'year': dd.year,
                                                                           'month': dd.month,
                                                                           'day': dd.day,
                                                                           'title': dd.budget_title,
                                                                           'budget_id': dd.budget_id,
                                                                           'budget_owner': dd.budget_owner,
                                                                           'total_budget': dd.total_budget,
                                                                           'day_data_zip': dd.day_data_zip,
                                                                           'category_zip': dd.category_zip,
                                                                           'categories_values': dd.categories_values,
                                                                           'categories_title': dd.categories_title,
                                                                           'categories_id': dd.categories_id,
                                                                           'div': mark_safe(dd.div),
                                                                           'script': mark_safe(dd.script),
                                                                           'day_sum': dd.day_sum,
                                                                           'day_avg': dd.day_avg,
                                                                           'category_percent': dd.category_percent})


@login_required
def budget_month_stats_detail(request, budget_id, year, month):
    dd = MonthViewBudget(request, year, month, budget_id)
    dd.month_calculation()
    dd.month_category_calculation()
    dd.month_figures_days()
    dd.month_figures_category()
    return render(request, 'core_sm/costs/budget/budget_month_detail.html', {'year': dd.year,
                                                                     'month': dd.month,
                                                                     'day_data': dd.day_data,
                                                                     'div': mark_safe(dd.div),
                                                                     'script': mark_safe(dd.script),
                                                                     'div_2': mark_safe(dd.div_2),
                                                                     'script_2': mark_safe(dd.script_2),
                                                                     'total_budget': dd.total_budget,
                                                                     'budget_owner': dd.budget_owner,
                                                                     'category_zip': dd.category_zip,
                                                                     'month_sum': dd.month_sum,
                                                                     'month_avg': dd.month_avg,
                                                                     'budget_title': dd.budget_title})

@login_required
def budget_year_stats_detail(request, id, year):
    budget_owner = User.objects.get(id=Budget.objects.get(id=id).user_id).username
    budget_year_title = Budget.objects.get(id=id).title
    total = Cost.objects.filter(budget_id=id, user=request.user).aggregate(Sum('value'))['value__sum']
    budget = Budget.objects.get(id=id).value

    try:
        total_budget = budget - total
    except TypeError:
        total_budget = 0

    Months = []
    Months_data = []
    Months_url = [str(x).zfill(2) for x in range(13)[1:]]
    year_month_calculation(Months)
    year_budget_calculation(Months_data, year, id, request)
    data = {
        'Miesiące': Months_url,
        'ZŁ': Months_data
    }
    p = Bar(data, values='ZŁ', label='Miesiące', legend=False, plot_width=910, plot_height=350, color='blue')
    script, div = components(p, CDN)
    all_data = zip(Months, Months_data, Months_url)
    year_sum = Cost.objects.filter(publish__year=year, budget_id=id, user=request.user).aggregate(Sum('value'))['value__sum']
    categories = []
    category_id = []

    for item in Category.objects.values('title', 'id'):
        categories.append(item['title'])
        category_id.append(item['id'])

    categories_data = []
    year_budget_categories_calculation(year, category_id, categories_data, id, request)
    data1 = {
        'money': [float(x) for x in categories_data],
        'labels': categories
    }
    p1 = Bar(data1, values='money', label='labels', legend=False, plot_width=920, plot_height=350, color='blue')
    script1, div1 = components(p1, CDN)
    categories_res = zip(categories, categories_data, category_id)
    return render(request, 'core_sm/costs/budget/budget_year_detail.html', {'year_sum': year_sum,
                                                                            'script': mark_safe(script),
                                                                            'div': mark_safe(div),
                                                                            'all_data': all_data,
                                                                            'script1': mark_safe(script1),
                                                                            'div1': mark_safe(div1),
                                                                            'categories_res': categories_res,
                                                                            'id': id,
                                                                            'year': year,
                                                                            'total_budget': total_budget,
                                                                            'budget_year_title' : budget_year_title,
                                                                            'budget_owner': budget_owner})


@login_required
def budget_detail(request, budget_id):
    budget_owner = User.objects.get(id=Budget.objects.get(id=budget_id).user_id).username
    title = Budget.objects.get(id=budget_id).title
    base = Cost.objects.filter(budget_id=budget_id, user=request.user).values()
    total = Cost.objects.filter(budget_id=budget_id, user=request.user).aggregate(Sum('value'))['value__sum']
    budget = Budget.objects.get(id=budget_id).value
    date = []
    date_url = []
    categories = []
    categories_id = []

    for item in Cost.objects.filter(budget_id=budget_id, user=request.user).values('title', 'publish', 'category_id'):
        date.append(str(item['publish']))
        date_url.append(str(item['publish']).replace('-', '/'))
        categories.append(Category.objects.get(id=item['category_id']).title)
        categories_id.append(Category.objects.get(id=item['category_id']).id)

    categories_title = []
    categories_title_id =[]
    categories_data = []

    for item in Category.objects.values('title', 'id'):
        categories_title.append(item['title'])
        categories_title_id.append(item['id'])

    budget_categories_calculation(budget_id, categories_title_id, categories_data, request)

    try:
        total_budget = budget - total
    except TypeError:
        total_budget = 0

    info = zip(base, date, date_url, categories, categories_id)


    data = {
        'money': [float(x) for x in categories_data],
        'labels': categories_title
    }
    p1 = Bar(data, values='money', label='labels', legend=False, plot_width=920, plot_height=350, color='blue')
    script, div = components(p1, CDN)

    cat_all = zip(categories_title, categories_data, categories_title_id)
    return render(request, 'core_sm/costs/budget/budget_detail.html', {'info': info,
                                                                'title': title,
                                                                'total': total,
                                                                'budget': budget,
                                                                'total_budget': total_budget,
                                                                'script': mark_safe(script),
                                                                'div': mark_safe(div),
                                                                'cat_all': cat_all,
                                                                'categories_data': categories_data,
                                                                'budget_owner': budget_owner})


@login_required
def budget_setup(request):
    add =False
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            add = True
            f = form.save(commit=False)
            f.user = request.user
            f.save()
    else:
        form = BudgetForm()

    budget_titles = []
    budget_values = []
    budget_id = []
    budget_created = []
    spendings_values = []

    for item in Budget.objects.filter(user_id=User.objects.get(username=request.user).id).values('title', 'value', 'id', 'publish'):
        budget_titles.append(item['title'])
        budget_values.append(item['value'])
        budget_id.append(item['id'])
        budget_created.append(str(item['publish']).replace('-', '/'))
        try:
            spendings_values.append(item['value'] - Cost.objects.filter(budget_id=item['id']).aggregate(Sum('value'))['value__sum'])
        except(TypeError):
            spendings_values.append(item['value'])

    all_data = zip(budget_titles, budget_values, spendings_values, budget_id, budget_created)
    return render(request, 'core_sm/costs/budget/budget_setup.html', {'add': add,
                                                         'form': form,
                                                         'all_data': all_data})


@login_required
def day_data_multiadd(request, no_of_lines=0):
    add = False
    no_of_lines = int(no_of_lines)
    CostFormSet = modelformset_factory(model=Cost, form=DataAddForm, extra=no_of_lines)
    if request.method == 'POST' and 'form' in request.POST:
        formset = CostFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset.forms:
                add = True
                f = form.save(commit=False)
                f.user = request.user
                f.save()
    else:
        formset = CostFormSet(queryset=Cost.objects.none())
        for item in formset:
            item.fields['category'].queryset=Category.objects.filter(user=request.user)
            item.fields['budget'].queryset=Budget.objects.filter(user=request.user)

    if request.method == 'POST' and 'no_line' in request.POST:
        generate_form = MultiaddGenerateForm(request.POST)
        if generate_form.is_valid():
            cd = generate_form.cleaned_data
            return HttpResponseRedirect(reverse('core_sm:day_data_multiadd', args=(cd['formy'], )))
    else:
        generate_form = MultiaddGenerateForm()

    return render(request, 'core_sm/costs/multi_add.html', {'formset': formset,
                                                            'no_of_lines': no_of_lines,
                                                            'generate_form': generate_form,
                                                            'add': add})


@login_required
def day_data_delete(request, id):
    Message = "Rekord '{}' został usunięty z bazy danych".format(Cost.objects.filter(id=id).values('title')[0]['title'])
    Cost.objects.filter(id=id).delete()
    return render(request, 'core_sm/costs/day_delete.html', {'Message': Message})


@login_required
def costs_stats(request):
    if request.method == "GET":
        form = DataGenerateForm()
    else:
        form = DataGenerateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('core_sm:month_stats_detail', args=(cd['year'], cd['month'])))
    return render(request, 'core_sm/costs/stats.html', {'form': form})


def current_detail(request):
    year = datetime.date.today().year
    month = str(datetime.date.today().month).zfill(2)
    day = str(datetime.date.today().day).zfill(2)
    return render(request, 'core_sm/costs/start.html', {'year': year,
                                                        'month': month,
                                                        'day': day})


@login_required
def stats_comp(request, date_x=datetime.date.today(), date_y=datetime.date.today()):
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

    data_sum = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Sum('value'))['value__sum']
    data_avg = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Avg('value'))['value__avg']
    data_min = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Min('value'))['value__min']
    data_max = Cost.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Max('value'))['value__max']

    comp_budget_title = []
    comp_budget_spends = []
    comp_budget_id = []
    for item in Budget.objects.values('title', 'id'):
        val = Cost.objects.filter(budget_id=item['id'], publish__range=(start_date, end_date), user=request.user).aggregate(Sum('value'))['value__sum']
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

    budgets_sum = Budget.objects.filter(publish__range=(start_date, end_date), user=request.user).aggregate(Sum('value'))['value__sum']
    total_cost_per_budget = sum(comp_budget_spends)

    try:
        total_budget = budgets_sum - total_cost_per_budget
    except TypeError:
        total_budget = 0

    return render(request, 'core_sm/costs/stats_comp.html', {'data': data,
                                                             'data_sum': data_sum,
                                                             'data_avg': data_avg,
                                                             'data_min': data_min,
                                                             'data_max': data_max,
                                                             'script': mark_safe(script),
                                                             'div': mark_safe(div),
                                                             'categories_res': categories_res,
                                                             'form': form,
                                                             'date_x': date_x,
                                                             'date_y': date_y,
                                                             'comp_budget_data': comp_budget_data,
                                                             'total_cost_per_budget': total_cost_per_budget,
                                                             'total_budget': total_budget,
                                                             'budgets_sum': budgets_sum})


@login_required
def year_stats_detail(request, year):
    dd = YearView(year, request)
    dd.year_calculation()
    dd.year_category_calculation()
    dd.year_budget_calculation()
    dd.year_figures_days()
    dd.year_figures_category()
    another = "/costs/{}/".format(int(year)+1)
    back = "/costs/{}".format(int(year)-1)
    return render(request, 'core_sm/costs/year_stats_detail.html', {'year': dd.year,
                                                                     'div': mark_safe(dd.div),
                                                                     'script': mark_safe(dd.script),
                                                                     'div_2': mark_safe(dd.div_2),
                                                                     'script_2': mark_safe(dd.script_2),
                                                                     'year_data_zip': dd.year_data_zip,
                                                                     'year_sum': dd.year_sum,
                                                                     'year_avg': sum(dd.month_data)/len(dd.month_data),
                                                                     'year_budget_data_zip': dd.year_budget_data_zip,
                                                                     'year_categories_data_zip': dd.year_categories_data_zip,
                                                                     'back': back,
                                                                    'another': another})


@login_required
def month_stats_detail(request, year, month):
    dd = MonthView(year, month, request)
    dd.month_calculation()
    dd.month_category_calculation()
    dd.month_budget_calculation()
    dd.month_figures_days()
    dd.month_figures_category()

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

    return render(request, 'core_sm/costs/month_stats_detail.html', {'year': dd.year,
                                                                     'month': dd.month,
                                                                     'day_data': dd.day_data,
                                                                     'div': mark_safe(dd.div),
                                                                     'script': mark_safe(dd.script),
                                                                     'div_2': mark_safe(dd.div_2),
                                                                     'script_2': mark_safe(dd.script_2),
                                                                     'category_zip': dd.category_zip,
                                                                     'budget_zip': dd.budget_zip,
                                                                     'month_sum': dd.month_sum,
                                                                     'month_avg': dd.month_avg,
                                                                     'back': back,
                                                                     'another': another})


@login_required
def day_stats_detail(request, year, month, day):
    dd = DayView(year, month, day, request)
    dd.day_calculation()
    dd.day_max_min()
    dd.day_figure()
    dd.back_next_day()
    return render(request, 'core_sm/costs/day_stats_detail.html', {'year': dd.year,
                                                                     'month': dd.month,
                                                                     'day': dd.day,
                                                                     'category_zip': dd.category_zip,
                                                                     'budget_zip': dd.budget_zip,
                                                                     'day_data': dd.day_data,
                                                                     'day_sum': dd.day_sum,
                                                                     'day_avg': dd.day_avg,
                                                                     'categories_id': dd.categories_id,
                                                                     'categories_title': dd.categories_title,
                                                                     'categories_sum': dd.categories_values,
                                                                     'budget_id': dd.budget_id,
                                                                     'budget_titles': dd.budget_titles,
                                                                     'budget_values': dd.budget_values,
                                                                     'day_max': dd.day_max,
                                                                     'day_min': dd.day_min,
                                                                     'script': mark_safe(dd.script),
                                                                     'div': mark_safe(dd.div),
                                                                     'back': dd.back,
                                                                     'another': dd.another,
                                                                     })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnianie zakonczylo sie sukcesem.')
                else:
                    return HttpResponse('Konto jest zablokowane')
            else:
                return HttpResponse('Nieprawidlowe dane uwierzytelniajace')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def test_view(request, year):
    dd = YearView(year, request)
    dd.year_calculation()
    dd.year_category_calculation()
    dd.year_budget_calculation()
    dd.year_figures_days()
    dd.year_figures_category()
    another = "/costs/{}/".format(int(year)+1)
    back = "/costs/{}".format(int(year)-1)
    return render(request, 'core_sm/costs/category/test_view.html', {'year': dd.year,
                                                                     'div': mark_safe(dd.div),
                                                                     'script': mark_safe(dd.script),
                                                                     'div_2': mark_safe(dd.div_2),
                                                                     'script_2': mark_safe(dd.script_2),
                                                                     'year_data_zip': dd.year_data_zip,
                                                                     'year_sum': dd.year_sum,
                                                                     'year_avg': sum(dd.month_data)/len(dd.month_data),
                                                                     'year_budget_data_zip': dd.year_budget_data_zip,
                                                                     'year_categories_data_zip': dd.year_categories_data_zip,
                                                                     'another': another,
                                                                     'back': back})