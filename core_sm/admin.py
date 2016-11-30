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
    list_display = ['title','january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
              'october', 'november', 'december']
    list_filter = ['title']
    list_editable = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
              'october', 'november', 'december']
admin.site.register(Budget, BudgetAdmin)

