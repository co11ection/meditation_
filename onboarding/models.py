from django.db import models


class OnboardingText(models.Model):
    content = models.TextField(verbose_name="Текст для обучения")
    order = models.PositiveIntegerField(default=0,
                                        verbose_name="Порядок отображения")
