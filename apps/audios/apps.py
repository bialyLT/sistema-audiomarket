from django.apps import AppConfig


class AudiosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.audios'
    verbose_name = 'Gestión de Audios'

    def ready(self):
        import apps.audios.signals
