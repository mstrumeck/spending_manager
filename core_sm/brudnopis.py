import datetime
import calendar
a = calendar.monthrange(2016,10)
mr = [x for x in range(a[1]+1)][1:]
print(mr)
print(a)
d = datetime.date(2016,10,23).year
dd = []
for item in mr:
    dd.append('2016-10-{}'.format(item))

print(dd[0])


