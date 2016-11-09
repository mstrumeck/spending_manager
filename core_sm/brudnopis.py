import datetime
import calendar
import decimal

a = calendar.monthrange(2016,10)
mr = [x for x in range(a[1]+1)][1:]
print(mr)
print(a)

print(calendar.month_name[3])
