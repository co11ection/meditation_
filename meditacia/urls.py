from rest_framework.routers import DefaultRouter
from django.urls import path

from . import views

app_name = 'meditacia'

router = DefaultRouter()
router.register('', views.MeditationsListView)

urlpatterns = [
    path('profiles', views.UserProfileMediation.as_view(), name='profiles'),
    path('start-meditation/<int:meditation_id>/',
         views.StartMeditationView.as_view(), name='start-meditation'),
    path('end-meditation/<int:meditation_id>/', views.EndMeditationView.as_view(),
         name='end-meditation'),

]
