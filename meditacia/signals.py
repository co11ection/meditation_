from django.contrib.auth import get_user_model

from users.models import CustomUser
from .models import Meditation, MeditationSession
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserProfile


@receiver(post_save, sender=MeditationSession)
def create_meditation_on_start(sender, instance, created, **kwargs):
    if created:
        Meditation.objects.create(
            name=f"Сеанс медитации {instance.start_time}",
            description="Описание медитации",
            duration=instance.meditation.duration,
            created_date=instance.start_time.date(),
        )


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=get_user_model())
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
