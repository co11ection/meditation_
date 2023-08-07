from django.contrib import admin
from .models import Meditation


# Register your models here.

class MeditationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'duration']
    list_filter = ['completed_by_users']
    search_fields = ['name', 'description']


admin.site.register(Meditation, MeditationAdmin)
