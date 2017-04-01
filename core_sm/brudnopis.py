class DayView(object):

    def __init__(self, year, month, day, category_id, budget_id):
        self.year = year
        self.month = month
        self.day = day
        self.category_id = category_id
        self.budget_id = budget_id
        self.data = []

    def storage(self):
        some_data =[]
        some_data_2 = []

    def total_2(self):
        for item in range(5):
            self.data.append(item)


dd = DayView(2016,2,5,1,2)
dd.total_2()
print(dd.data)


