from wallet.models import WalletTokens


def calculate_group_meditation_tokens(group_size):
    if group_size > 2000:
        return 3.0
    elif group_size > 1000:
        return 2.5
    elif group_size > 500:
        return 2.2
    elif group_size > 300:
        return 1.9
    elif group_size > 200:
        return 1.7
    elif group_size > 100:
        return 1.5
    elif group_size > 50:
        return 1.3
    elif group_size > 40:
        return 1.25
    elif group_size > 30:
        return 1.2
    elif group_size > 20:
        return 1.15
    elif group_size > 10:
        return 1.1
    elif group_size > 1:
        return 1.05
    else:
        return 1.0


def get_balance(user):
    """
    Получение баланса пользователя из базы данных.
    """
    try:
        wallet_tokens = WalletTokens.objects.get(user=user)
        return wallet_tokens.balance
    except:
        return None
