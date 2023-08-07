from django.contrib import admin

from onboarding.models import ChatMessage, OnboardingText, Complaint


# Register your models here.

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
