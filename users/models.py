from django.db import models


class Users(models.Model):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
    )
    username = models.CharField(max_length=500, blank=True, null=True)
    login = models.CharField(max_length=100, blank=True, null=True,
                             verbose_name='Логин', unique=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    token = models.CharField(max_length=500, blank=True, null=True,
                             unique=True, verbose_name='Токен авторизации')
    photo = models.ImageField(null=True, blank=True, upload_to="media/",
                              verbose_name='Аватарка')
    is_active = models.BooleanField(blank=True, default=True,
                                    verbose_name='Статус блокировки')
    phone_number = models.CharField(max_length=100, blank=True, null=True,
                                    verbose_name='Телефон', unique=True)
    email = models.CharField(max_length=100, blank=True, null=True,
                             verbose_name='Почта')
    role = models.CharField(default='user', choices=ROLE_CHOICES,
                            max_length=12)
    sms_code = models.IntegerField(blank=True, null=True)
    fcm_token = models.CharField(max_length=500, null=True, blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

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

    @property
    def is_user(self):
        return self.role == 'user'

    def __str__(self):
        return f"{self.username}"


class CodePhone(models.Model):
    login = models.CharField(max_length=100, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    is_confirmed = models.BooleanField(max_length=100, blank=True, null=True,
                                       default=False)
    time = models.DateTimeField(auto_now=True)
