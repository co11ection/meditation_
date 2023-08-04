from django.urls import path

from .views import ChatMessageView
from .views import ComplaintView
from .views import OnboardingTextAPIView, OnboardingTextDetailView

urlpatterns = [
    path('', OnboardingTextAPIView.as_view(),
         name='onboarding-text-list'),
    path('<int:pk>', OnboardingTextDetailView.as_view(),
         name='onboarding-text-detail'),
    path('complaints/', ComplaintView.as_view(), name='complaint-list-create'),
    path('chat-messages/', ChatMessageView.as_view(),
         name='chat-message-list-create'),

]
