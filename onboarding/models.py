from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class OnboardType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название типа онбординга")
    slug = models.SlugField(
        max_length=250, unique=True, db_index=True, verbose_name="URL"
    )

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("onboarding-by-type", args=[str(self.slug)])

    class Meta:
        verbose_name = "Тип онбординга"
        verbose_name_plural = "Типы онбордингов"


class OnboardText(models.Model):
    content = models.TextField(verbose_name="Текст")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")
    type = models.ForeignKey(
        OnboardType, on_delete=models.CASCADE, verbose_name="Тип онбординга"
    )

    def __str__(self):
        return f"Ваш текст {self.content}, он будет отображен по очереди {self.order}"

    class Meta:
        ordering = ["order"]
        verbose_name = "Текст онбординга"
        verbose_name_plural = "Тексты для онбординга"
        unique_together = ["content", "order"]
