from django.db import models


class OnboardingTextStartApp(models.Model):
    content = models.TextField(verbose_name="Текст для начала в приложение")
    order = models.PositiveIntegerField(default=0,
                                        verbose_name="Порядок отображения")

    class Meta:
        ordering = ['order']
        verbose_name = "Текст для начала в приложении"
        verbose_name_plural = "Тексты для начала в приложении"
        unique_together = ['content', 'order']


class OnboardingTextStartMeditation(models.Model):
    content = models.TextField(verbose_name="Текст перед медитацией")
    order = models.PositiveIntegerField(default=1,
                                        verbose_name="Порядок отображения")

    class Meta:
        ordering = ['order']
        verbose_name = "Текст для старта в медитации"
        verbose_name_plural = "Тексты для старта в медитации"
        unique_together = ['content', 'order']
