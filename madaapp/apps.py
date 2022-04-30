from django.apps import AppConfig


class MadaappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'madaapp'

    def ready(self):
        import madaapp.signals
