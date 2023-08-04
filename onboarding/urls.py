from django.urls import path
from .views import OnboardingTextAPIView, OnboardingTextDetailView

urlpatterns = [
    path('', OnboardingTextAPIView.as_view(),
         name='onboarding-text-list'),
    path('<int:pk>', OnboardingTextDetailView.as_view(),
         name='onboarding-text-detail'),
]
