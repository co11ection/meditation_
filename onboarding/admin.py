from django.contrib import admin
from .models import OnboardText, OnboardType


@admin.register(OnboardType)
class OnboardTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    list_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(OnboardText)
class OnboardTextAdmin(admin.ModelAdmin):
    list_display = ("content", "order", "type")
    list_filter = ("type",)
    search_fields = ("content",)
    ordering = ("order",)
