from .models import Meditation
from django.contrib import admin
from .models import UserProfile


# Register your models here.

class MeditationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'duration']
    list_filter = ['completed_by_users']
    search_fields = ['name', 'description']


admin.site.register(Meditation, MeditationAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'practice_time', 'daily_practice', 'continuous_practice',
        'progress_accelerator', 'engaged_followers')
    list_filter = (
        'daily_practice', 'continuous_practice', 'progress_accelerator')
    search_fields = ('user__nickname', 'user__login',
                     'user__email')
