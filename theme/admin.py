from django.contrib import admin

from .models import Theme

class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'file_name', 'default')

admin.site.register(Theme, ThemeAdmin)
