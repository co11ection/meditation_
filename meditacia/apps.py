from django.apps import AppConfig


class MeditaciaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "meditacia"

    def ready(self):
        import meditacia.signals
