from django.urls import path

from wallet import views
from wallet.views import WalletTokensView

app_name = "wallet"

urlpatterns = [
    # path('gift_token/', views.send_tokens_to_user, name='send_tokens_to_user'),
    # path('hello/', views.hello, name='hello'),
    path("balance/", WalletTokensView.as_view()),
    path("balance1/", WalletTokensView.calculate_individual_tokens_to_earn),
]
