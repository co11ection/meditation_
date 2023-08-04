from django.db import models


class Meditation(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название медитации')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    duration = models.DurationField(verbose_name='Длительность медитации')
    completed_by_users = models.ManyToManyField('Users', blank=True,
                                                related_name='completed_meditations')
