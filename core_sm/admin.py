from django.contrib import admin
from .models import Cost, Budget, Category


class CostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'category',  'publish', 'updated']
    list_filter = ['title', 'category', 'created']
    list_editable = ['value',  'category']
    search_fields = ['title', 'category', 'publish']
    date_hierarchy = 'publish'
    ordering = ['category', 'publish']
admin.site.register(Cost, CostsAdmin)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ['title', 'value']
    list_filter = ['title']
    list_editable = ['value']
admin.site.register(Budget, BudgetAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(Category, CategoryAdmin)