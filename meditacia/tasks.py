from celery import shared_task
from .models import Meditation


@shared_task
def end_meditation(meditation_id):
    meditation = Meditation.objects.get(id=meditation_id)
    # Do whatever you need to do when the meditation ends,
    # such as calculating earned tokens, etc.
    meditation.completed = True
    meditation.save()
