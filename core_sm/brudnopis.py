import datetime
import calendar
import decimal
a = calendar.monthrange(2016,10)
mr = [x for x in range(a[1]+1)][1:]
print(mr)
print(a)
d = datetime.date(2016,10,23).year
dd = []
for item in mr:
    dd.append('2016-10-{}'.format(item))

b = [23,23,23,23]
c = [24,24,24,24]
d = [25,25,25,25]
e = [26,26,26,26]

master_data = zip(b,c,d,e)
print(master_data)
for data_1, data_2, data_3, data_4 in master_data:
    print(data_1,data_2,data_3,data_4)
day_numbers = [x for x in range(mr[1] + 1)][1:]



