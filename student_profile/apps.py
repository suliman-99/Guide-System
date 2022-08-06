from django.apps import AppConfig


class CvConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student_profile'

    def ready(self) -> None:
        import student_profile.signals.handlers
