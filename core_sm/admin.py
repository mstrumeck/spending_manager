from django.contrib import admin
from .models import Cost, DateMonthYear


class CostsAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'category', 'date', 'publish', 'updated']
    list_filter = ['title', 'category', 'created']
    list_editable = ['value', 'date', 'category']
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ['title', 'category', 'publish']
    date_hierarchy = 'publish'
    ordering = ['category', 'publish']
admin.site.register(Cost, CostsAdmin)

class DateMonthYearAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    list_filter = ['title']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title']
admin.site.register(DateMonthYear, DateMonthYearAdmin)