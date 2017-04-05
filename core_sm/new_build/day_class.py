from django.db.models import Avg, Max, Min, Sum
from core_sm.models import Cost, Budget, Category
from bokeh.embed import components
from bokeh.charts import Bar, Line, Donut
from bokeh.resources import CDN


class DayView(object):

    def __init__(self, year, month, day, request):
        """Init data"""
        self.year = year
        self.month = month
        self.day = day
        self.request = request
        self.day_data_conf = {}
        self.day_data = Cost.objects.filter(publish__year=year, publish__month=month, publish__day=day, user=request.user.id)
        self.script = None
        self.div = None
        '''DATA CONTAINERS'''
        self.title = []
        self.value =[]
        self.category = []
        self.budget = []
        self.cost_id = []
        self.day_sum = self.day_data.aggregate(Sum('value'))['value__sum']
        self.day_avg = self.day_data.aggregate(Avg('value'))['value__avg']
        self.day_max = 0
        self.day_min = 0
        self.categories_title = []
        self.categories_id = []
        self.categories_sum = []
        self.budget_titles = []
        self.budget_values = []
        self.budget_id = []
        '''ZIP Data'''
        self.category_zip = zip(self.categories_title, self.categories_sum, self.categories_id)
        self.budget_zip = zip(self.budget_titles, self.budget_values, self.budget_id)

    def day_calculation(self):
        for item in self.day_data.values('title', 'value', 'category_id', 'id', 'budget_id'):
            self.title.append(item['title'])
            self.value.append(float(item['value']))
            self.category.append(Category.objects.get(id=item['category_id']).title)
            self.cost_id.append(item['id'])
            self.budget.append(Budget.objects.get(id=item['budget_id']).title)

        for item in Category.objects.filter(user_id=self.request.user.id).values('title', 'id'):
            val = Cost.objects.filter(publish__year=self.year, publish__month=self.month, publish__day=self.day, user=self.request.user,
                                      category_id=item['id']).aggregate(Sum('value'))['value__sum']
            if val is not None:
                self.categories_sum.append(val)
                self.categories_title.append(item['title'])
                self.categories_id.append(item['id'])
            else:
                pass

        for item in Budget.objects.filter(user_id=self.request.user.id).values('title', 'id'):
            val = Cost.objects.filter(budget_id=item['id'], publish__year=self.year, publish__month=self.month, publish__day=self.day,
                                      user_id=self.request.user.id).aggregate(Sum('value'))['value__sum']
            if val is not None:
                self.budget_titles.append(item['title'])
                self.budget_values.append(val)
                self.budget_id.append(item['id'])
            else:
                pass

        return self.title, self.value, self.category, self.cost_id, self.budget, \
               self.categories_title, self.categories_id, self.categories_sum

    def day_max_min(self):
        try:
            self.day_max = [self.title[self.value.index(max(self.value))], max(self.value), self.category[self.value.index(max(self.value))],
                       self.budget[self.value.index(max(self.value))]]
        except(ValueError, TypeError):
            self.day_max = 0

        try:
            self.day_min = [self.title[self.value.index(min(self.value))], min(self.value), self.category[self.value.index(min(self.value))],
                       self.budget[self.value.index(min(self.value))]]
        except(ValueError, TypeError):
            self.day_min = 0
        return self.day_max, self.day_min

    def day_figure(self):
        if not self.categories_title:
            self.script = "<h2>Aby wykres się pojawił, musisz dodać jakiś wydatek</h2>"
            self.div = "<h1>Brak wydatków!</h1>"
            return self.script
        else:
            percent = []
            for item in self.categories_sum:
                val = 100 * float(item / (sum(self.categories_sum)))
                percent.append(val)

            data = {
                'money': percent,
                'label': self.categories_title
            }

            p = Donut(data, values='money', label='label')
            p.logo = None
            p.toolbar_location = None
            self.script, self.div = components(p, CDN)
        return self.script, self.div

