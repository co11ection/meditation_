from django.urls import path
from . import views

urlpatterns = [
    path('', views.meditations_list, name='meditations_list'),
]
