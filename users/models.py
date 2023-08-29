from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, \
    BaseUserManager
from django.db import models

from wallet.models import WalletTokens


class CustomUserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The Login field must be set')

        extra_fields.setdefault('is_active', True)
        user = self.model(login=login, **extra_fields)
        if password is not None:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(login, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
    )
    login = models.CharField(max_length=100, unique=True, verbose_name='Логин')
    nickname = models.CharField(max_length=100, blank=True, null=True, verbose_name='Никнейм')
    password = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=500, blank=True, null=True,
                             unique=True, verbose_name='Токен авторизации')
    code = models.IntegerField(blank=True, null=True)
    photo = models.ImageField(null=True, blank=True, upload_to="media/",
                              verbose_name='Аватарка')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True,
                                    verbose_name='Статус активности')
    phone_number = models.CharField(max_length=100, blank=True, null=True,
                                    verbose_name='Телефон', unique=True)
    email = models.CharField(max_length=100, blank=True, null=True,
                             verbose_name='Почта')
    fcm_token = models.CharField(max_length=500, null=True, blank=True)
    consecutive_meditation_days = models.IntegerField(default=0,
                                                      verbose_name='Дни непрерывной медитации')
    role = models.CharField(default='user', choices=ROLE_CHOICES,
                            max_length=12)

    objects = CustomUserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def send_tokens_to_user(self, recipient, amount):
        sender_wallet, _ = WalletTokens.objects.get_or_create(user=self)
        recipient_wallet, _ = WalletTokens.objects.get_or_create(user=recipient)

        if sender_wallet.balance >= amount:
            sender_wallet.balance -= amount
            recipient_wallet.balance += amount

            sender_wallet.save()
            recipient_wallet.save()
            return True
        else:
            return False

    @property
    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return f"{self.nickname}"


class CodePhone(models.Model):
    login = models.CharField(max_length=100, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    is_confirmed = models.BooleanField(max_length=100, blank=True, null=True,
                                       default=False)
    time = models.DateTimeField(auto_now=True)
