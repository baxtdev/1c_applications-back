from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user'
    verbose_name = 'Пользователи и Персональные данные'
    def ready(self) -> None:
        import apps.user.signals