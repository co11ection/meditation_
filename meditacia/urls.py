from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import MeditationsListView, StartMeditationView, EndMeditationView, \
    UserProfileUpdateView

app_name = 'meditacia'

router = DefaultRouter()
router.register('', MeditationsListView)

urlpatterns = [
    *router.urls,
    path('start-meditation/<int:meditation_id>/',
         StartMeditationView.as_view(), name='start-meditation'),
    path('profile/', UserProfileUpdateView.as_view(),
         name='user-profile-update'),
    path('end-meditation/<int:meditation_id>/', EndMeditationView.as_view(),
         name='end-meditation'),

]
