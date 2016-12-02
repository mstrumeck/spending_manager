from django.contrib import admin
from .models import Cost, Budget


class CostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'category',  'publish', 'updated']
    list_filter = ['title', 'category', 'created']
    list_editable = ['value',  'category']
    search_fields = ['title', 'category', 'publish']
    date_hierarchy = 'publish'
    ordering = ['category', 'publish']
admin.site.register(Cost, CostsAdmin)

class BudgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'year', 'month']
    list_filter = ['title', 'year', 'month']
    list_editable = ['value', 'year', 'month']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Budget, BudgetAdmin)

