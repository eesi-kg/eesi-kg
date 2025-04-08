from django.apps import AppConfig


class RealEstateConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.real_estate'
    verbose_name = "НЕДВИЖИМОСТЬ"

    def ready(self):
        import applications.real_estate.signals
