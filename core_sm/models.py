from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime


class Budget(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField(default=datetime.date(datetime.datetime.now().year, 1, 1), unique=True)
    end_date = models.DateField(default=datetime.date(datetime.datetime.now().year, 12, 31), unique=True)
    january = models.DecimalField(decimal_places=2, max_digits=10)
    february = models.DecimalField(decimal_places=2, max_digits=10)
    march = models.DecimalField(decimal_places=2, max_digits=10)
    april = models.DecimalField(decimal_places=2, max_digits=10)
    may = models.DecimalField(decimal_places=2, max_digits=10)
    june = models.DecimalField(decimal_places=2, max_digits=10)
    july = models.DecimalField(decimal_places=2, max_digits=10)
    august = models.DecimalField(decimal_places=2, max_digits=10)
    september = models.DecimalField(decimal_places=2, max_digits=10)
    october = models.DecimalField(decimal_places=2, max_digits=10)
    november = models.DecimalField(decimal_places=2, max_digits=10)
    december = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        ordering = ('-start_date',)

    def budget_year(self):
        total += (self.january + self.february + self.march + self.april + self.may + self.june + self.july + self.august +
                   self.september + self.october + self.november + self.december)
        return total

    def __str__(self):
        return self.title


class Cost(models.Model):
    STATUS_CHOICES = [
        ['Domowe', 'Domowe'],
        ['Jedzenie', 'Jedzenie'],
        ['Kosmetyki i Chemia', 'Kosmetyki i Chemia'],
        ['Rozrywka', 'Rozrywka'],
        ['Okazyjne', 'Okazyjne'],
        ['Inne', 'Inne']
    ]

    title = models.CharField(max_length=200, db_index=True)
    publish = models.DateField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('core_sm:stats_detail', args=[self.publish.year,
                                            self.publish.strftime('%y'),
                                            self.publish.strftime('%m'),
                                            self.publish.strftime('%d')])

    def __str__(self):
        return self.title