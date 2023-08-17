from django.contrib import admin
from .models import OnboardingText


@admin.register(OnboardingText)
class OnboardingTextAdmin(admin.ModelAdmin):
    list_display = ('content', 'order')
    list_display_links = ('content',)
    list_editable = ('order',)
