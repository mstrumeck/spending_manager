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
print(type(datetime.date(2016,10,2).year))