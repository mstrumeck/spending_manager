from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime


class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ('-title',)

    def __str__(self):
        return self.title

    def get_absolute_ur(self):
        return reverse('core_sm:category_detail', args=[self.id])


class Budget(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    value = models.DecimalField(decimal_places=2, max_digits=10)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core_sm:budget_detail', args=[self.id])


class Cost(models.Model):
    budget = models.ForeignKey(Budget, related_name='cost')
    category = models.ForeignKey(Category, related_name='cost')
    title = models.CharField(max_length=200, db_index=True)
    publish = models.DateField(default=timezone.now)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):
        return reverse('core_sm:stats_detail', args=[self.publish.year,
                                            self.publish.strftime('%y'),
                                            self.publish.strftime('%m'),
                                            self.publish.strftime('%d')])

    def __str__(self):
        return self.title