from django.db import models


class WalletTokens(models.Model):
    user = models.OneToOneField('users.CustomUser',
                                verbose_name='Кошелек пользователя',
                                on_delete=models.CASCADE)
    balance = models.DecimalField(verbose_name='Баланс', max_digits=10,
                                  decimal_places=2,
                                  default=0)
    date_add_tokens = models.DateTimeField(auto_now_add=True, blank=True,
                                           null=True,
                                           verbose_name='Дата добавления токенов')

    class Meta:
        app_label = 'wallet'
        db_table = 'wallet_tokens'
        verbose_name = 'Баланс токенов пользователя'
        verbose_name_plural = 'Баланс токенов пользователей'
