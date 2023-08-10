from django.db import models

from users.models import CustomUser


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


class OnboardingStep(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название этапа')
    description = models.TextField(verbose_name='Описание этапа')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Этап онбординга'
        verbose_name_plural = 'Этапы онбординга'


class UserOnboarding(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    completed_steps = models.ManyToManyField(OnboardingStep,
                                             verbose_name='Пройденные этапы')
    skipped = models.BooleanField(default=False,
                                  verbose_name='Пропущен онбординг')

    class Meta:
        verbose_name = 'Прохождение онбординга'
        verbose_name_plural = 'Прохождения онбординга'


class ChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время создания')

    def __str__(self):
        return f"{self.user.nickname}: {self.message}"

    class Meta:
        verbose_name = 'Сообщение чата'
        verbose_name_plural = 'Сообщения чата'


class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст жалобы')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время создания')

    def __str__(self):
        return f"{self.user.nickname}: {self.text}"

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
