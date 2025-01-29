from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "API.users"

    def ready(self):
        import API.users.signals  # Ajuste também para 'API.users.signals' se quiser ser consistente
