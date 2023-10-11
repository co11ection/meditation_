from django.contrib import admin
from .models import Meditation, UserProfile, GroupMeditation


# Register your models here.
@admin.register(Meditation)
class MeditationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "duration"]
    list_filter = ["completed_by_users"]
    search_fields = ["name", "description"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "practice_time",
        "daily_practice",
        "continuous_practice",
        "progress_accelerator",
        "engaged_followers",
    )
    list_filter = ("daily_practice", "continuous_practice", "progress_accelerator")
    search_fields = ("user__nickname", "user__login", "user__email")


@admin.register(GroupMeditation)
class GroupMeditationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "author",
        "start_datetime",
        "duration",
        "max_participants",
        "created_at",
    ]
