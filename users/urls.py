from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('registration_get_code/', views.registration_get_code, name='registration_get_code'),
    path('registration/', views.registration, name='registration'),
    path('calculate_tokens/', views.calculate_tokens, name='calculate_tokens'),
    path('api/users/<int:pk>/', views.user_profile, name='user_profile'),
    path('auth/', views.auth, name='authentication'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('check_code/', views.check_code, name='check_code'),
    path('reset_password_confirm/', views.reset_password_confirm, name='reset_password_confirm'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('change_photo/', views.change_photo, name='change_photo'),
    # path('delete_user', views.delete_user),
    # path('state', views.get_state),
    # path('user_fcm', views.fcm_user),
    # path('update_user', views.update_user),
    # path('put_phone', views.put_phone),
    # path('info', views.get_info),
    # path('offer', views.get_offer),
    # path('politic', views.get_pol),
    # path('get_confidential', views.get_conf),
]
