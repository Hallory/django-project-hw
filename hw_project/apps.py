from django.apps import AppConfig



class HwProjectConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hw_project"

    def ready(self):
        import hw_project.signals  # noqa: F401