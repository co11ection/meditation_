from django.urls import path
from .views import OnboardingTextView

urlpatterns = [
    path('text/', OnboardingTextView.as_view(), name='onboarding-text')

    # Добавьте другие URL-маршруты по мере необходимости
]
