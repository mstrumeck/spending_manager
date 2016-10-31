from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

class DateMonthYear(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'DateMonthYear'
        verbose_name_plural = 'DatesMonthsYears'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core_sm:cost_list_by_datemonthyear', args=[self.slug])


class Cost(models.Model):
    STATUS_CHOICES = (
        ('Domowe', 'Domowe'),
        ('Jedzenie', 'Jedzenie'),
        ('Kosmetyki i Chemia', 'Kosmetyki i Chemia'),
        ('Rozrywka', 'Rozrywka'),
        ('Okazyjne', 'Okazyjne'),
        ('Inne', 'Inne')
    )
    date = models.ForeignKey(DateMonthYear, related_name='costs')
    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique_for_date='publish', db_index=True)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=STATUS_CHOICES)

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('core_sm:stats_detail', args=[self.publish.year,
                                            self.publish.strftime('%m')])

    def __str__(self):
        return self.title