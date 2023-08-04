from django.db import models


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
