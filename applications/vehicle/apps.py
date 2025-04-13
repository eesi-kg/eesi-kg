from django.apps import AppConfig


class VehicleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.vehicle'
    verbose_name = "6. ТРАНСПОРТ"

    def ready(self):
        import applications.vehicle.signals
        