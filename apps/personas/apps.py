from django.apps import AppConfig


class PersonasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.personas'

    def ready(self):
        # Importamos las señales para que Django las registre al iniciar
        import apps.personas.signals
