from django.db import models
from django.utils import timezone

from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    practice_time = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="Время практики"
    )
    daily_practice = models.BooleanField(
        blank=True, null=True, default=False, verbose_name="Ежедневная практика"
    )
    continuous_practice = models.IntegerField(
        blank=True, null=True, default=0, verbose_name="Непрерывная практика"
    )
    progress_accelerator = models.BooleanField(
        blank=True, null=True, default=False, verbose_name="Ускоритель прогресса"
    )
    engaged_followers = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="Приглашенные подписчики"
    )

    class Meta:
        verbose_name = "Профиль Пользователя"
        verbose_name_plural = "Профиль Пользователя"

    def __str__(self):
        return str(self.user)


class Meditation(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название медитации")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    duration = models.DurationField(verbose_name="Длительность медитации")
    completed_by_users = models.ManyToManyField(
        "users.CustomUser", blank=True, related_name="completed_meditations"
    )
    created_date = models.DateField(verbose_name="Дата создания медитации")

    class Meta:
        verbose_name = "Медитация"
        verbose_name_plural = "Медитации"


class MeditationSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=[("active", "Active"), ("paused", "Paused")]
    )

    def __str__(self):
        return f"{self.user.nickname} - {self.meditation.name}"


class GroupMeditation(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Название медитации")
    participants = models.ManyToManyField(
        User, related_name="group_meditations", blank=True
    )
    start_datetime = models.DateTimeField(blank=True, null=True)
    max_participants = models.PositiveIntegerField()
    duration = models.DurationField(verbose_name="Длительность медитации")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Групповая медитация"
        verbose_name_plural = "Групповые медитации"
