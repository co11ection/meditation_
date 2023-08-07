from django.urls import path
from . import views

app_name = 'meditacia'

urlpatterns = [
    path('', views.meditations_list, name='meditations_list'),
]
