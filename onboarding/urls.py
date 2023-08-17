from django.urls import path
from .views import OnboardStartAppView, OnboardStartMeditationView

urlpatterns = [
    path('text-startapp/', OnboardStartAppView.as_view(), name='startapp'),
    path('text-startmeditation/', OnboardStartMeditationView.as_view(),
         name='startmeditation'),
]
