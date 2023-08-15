from django.urls import path

from wallet import views

app_name = 'wallet'

urlpatterns = [
    path('gift_token/', views.send_tokens_to_user, name='send_tokens_to_user'),
]
