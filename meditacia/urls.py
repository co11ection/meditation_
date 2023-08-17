from django.urls import path
from .views import MeditationsListView, StartMeditationView

app_name = 'meditacia'

urlpatterns = [
    path('', MeditationsListView.as_view(),
         name='meditations_list'),
    path('start-meditation/<int:meditation_id>/',
         StartMeditationView.as_view(), name='start_meditation'),
]
