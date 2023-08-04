from django.db import models

from users.models import Users


# Create your models here.
class OnboardingText(models.Model):
    part_number = models.PositiveIntegerField(unique=True,
                                              verbose_name='Номер страницы')
    title = models.CharField(max_length=255, verbose_name='Заголовок страницы')
    content = models.TextField(verbose_name='Содержание страницы')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Текст Онбординга'
        verbose_name_plural = 'Тексты Онбординга'


class ChatMessage(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время создания')

    def __str__(self):
        return f"{self.user.username}: {self.message}"

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'


class Complaint(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст жалобы')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время создания')

    def __str__(self):
        return f"{self.user.username}: {self.text}"

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'


class Moderator(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE,
                                verbose_name='Пользователь')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Модератор'
        verbose_name_plural = 'Модераторы'


class Administrator(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE,
                                verbose_name='Пользователь')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Администратор'
        verbose_name_plural = 'Администраторы'
