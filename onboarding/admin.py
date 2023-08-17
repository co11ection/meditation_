from django.contrib import admin
from .models import OnboardingTextStartApp, OnboardingTextStartMeditation


class OnboardingTextStartAppAdmin(admin.ModelAdmin):
    list_display = ('content', 'order')
    list_editable = ('order',)
    search_fields = ('content',)
    list_per_page = 20


class OnboardingTextStartMeditationAdmin(admin.ModelAdmin):
    list_display = ('content', 'order')
    list_editable = ('order',)
    search_fields = ('content',)
    list_per_page = 20


admin.site.register(OnboardingTextStartApp, OnboardingTextStartAppAdmin)
admin.site.register(OnboardingTextStartMeditation,
                    OnboardingTextStartMeditationAdmin)
