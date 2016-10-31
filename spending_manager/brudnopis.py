import calendar
import pprint

cal = calendar.TextCalendar(calendar.MONDAY)
a = cal.prmonth(2016, 10)
b = calendar.monthcalendar(2016, 10)

c = calendar.monthrange(2016,10)

d = [str(x) for x in range(c[1])]

for item in d:
    print(type(item))
