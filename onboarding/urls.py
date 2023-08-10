from django.urls import path

from . import views
from .views import OnboardingTextAPIView, OnboardingTextDetailView, \
    ChatMessageView, ComplaintView

urlpatterns = [
    path('onboarding-text/', OnboardingTextAPIView.as_view(),
         name='onboarding-text-list-create'),
    path('onboarding-text/<int:pk>/', OnboardingTextDetailView.as_view(),
         name='onboarding-text-detail'),
    path('chat-message/', ChatMessageView.as_view(),
         name='chat-message-list-create'),
    path('complaint/', ComplaintView.as_view(), name='complaint-list-create'),
    path('onboarding/steps/', views.OnboardingStepAPIView.as_view(),
         name='onboarding-steps'),
    path('user/onboarding/<int:user_id>/',
         views.UserOnboardingAPIView.as_view(), name='user-onboarding'),

]
