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

