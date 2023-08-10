from django.contrib import admin

from onboarding.models import ChatMessage, OnboardingText, Complaint

from .models import OnboardingStep, UserOnboarding


@admin.register(OnboardingStep)
class OnboardingStepAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')


@admin.register(UserOnboarding)
class UserOnboardingAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_completed_steps', 'skipped')
    list_filter = ('skipped',)
    search_fields = ('user__username', 'user__email')

    def get_completed_steps(self, obj):
        return ', '.join([step.title for step in obj.completed_steps.all()])

    get_completed_steps.short_description = 'Пройденные этапы'


class OnboardingTextAdmin(admin.ModelAdmin):
    list_display = ['part_number', 'title', 'content']


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message']
    list_filter = ['created_at']


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'text']


admin.site.register(OnboardingText, OnboardingTextAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)
admin.site.register(Complaint, ComplaintAdmin)
