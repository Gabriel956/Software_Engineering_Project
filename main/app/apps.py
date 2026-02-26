from django.apps import AppConfig

# App configuration for the app
class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals  # Import the signals module to connect the signal handlers
