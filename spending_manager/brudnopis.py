import datetime
import calendar

a = calendar.monthrange(2016,10)
mr = [x for x in range(a[1]+1)][1:]
print(mr)
print(a)

p = figure(title="Wykres dla {}.{}".format(year, month), x_axis_label='Dni miesiąca',
           y_axis_label='ZŁ', plot_width=1250, plot_height=400, background_fill_color="#E8DDCB")
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
       fill_color="#036564", line_color="#033649"))
