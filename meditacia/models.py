from django.db import models
from django.utils import timezone

from users.models import CustomUser


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    practice_time = models.PositiveIntegerField(blank=True, null=True, default=0)
    daily_practice = models.BooleanField(blank=True, null=True ,default=False)
    continuous_practice = models.IntegerField(blank=True, null=True, default=0)
    progress_accelerator = models.BooleanField(blank=True, null=True, default=False)
    engaged_followers = models.PositiveIntegerField(blank=True, null=True, default=0)

    class Meta:
        verbose_name = 'Профиль Пользователя'
        verbose_name_plural = 'Профиль Пользователя'

    def __str__(self):
        return str(self.user)


class Meditation(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название медитации')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    duration = models.DurationField(verbose_name='Длительность медитации')
    completed_by_users = models.ManyToManyField('users.CustomUser', blank=True,
                                                related_name='completed_meditations')
    created_date = models.DateField(verbose_name='Дата создания медитации')

    class Meta:
        verbose_name = 'Медитация'
        verbose_name_plural = 'Медитации'


class MeditationSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    meditation = models.ForeignKey(Meditation, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[("active", "Active"),
                                                      ("paused", "Paused")])

    def __str__(self):
        return f"{self.user.nickname} - {self.meditation.name}"
