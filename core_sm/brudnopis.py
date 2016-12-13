import datetime
import calendar
import decimal


a = calendar.monthrange(2016,10)
mr = [x for x in range(a[1]+1)][1:]
print(mr)
print(a)

print(calendar.month_name[3])

b = range(13)[1:]
b = [datetime.date(2016, x, 1) for x in b]

c = [x for x in range(13)[1:]]
print(datetime.date.today().year)

print(datetime.date.today() - datetime.timedelta(days=3*365))
d = str([(datetime.date.today() - datetime.timedelta(days=x*365)).year for x in range(10)])
print(d)
print(type(datetime.date(2016, 10, 2)))

STATUS_CHOICES = [
        ['Domowe', 'Domowe'],
        ['Jedzenie', 'Jedzenie'],
        ['Kosmetyki i Chemia', 'Kosmetyki i Chemia'],
        ['Rozrywka', 'Rozrywka'],
        ['Okazyjne', 'Okazyjne'],
        ['Inne', 'Inne']
    ]

STATUS_CHOICES += (('Kino', 'Kino'),)
categories = []
for item in STATUS_CHOICES:
    print(item[0])
    categories.append(item[0])

print(datetime.datetime.now().month)
print(datetime.datetime.now().year)
mr = calendar.monthrange(int(2016), int(5))
print(mr[1])
