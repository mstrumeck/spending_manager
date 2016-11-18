from django.contrib import admin
from .models import Cost


class CostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'category',  'publish', 'updated']
    list_filter = ['title', 'category', 'created']
    list_editable = ['value',  'category']
    search_fields = ['title', 'category', 'publish']
    date_hierarchy = 'publish'
    ordering = ['category', 'publish']
admin.site.register(Cost, CostsAdmin)

