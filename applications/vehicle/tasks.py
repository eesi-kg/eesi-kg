from celery import shared_task

from applications.vehicle.models import VehicleAd


@shared_task
def async_regenerate_qr(ad_id):
    ad = VehicleAd.objects.get(pk=ad_id)
    ad.regenerate_qr_code()
