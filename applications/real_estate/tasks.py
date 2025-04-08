from celery import shared_task

from applications.real_estate.models import RealEstateAd


@shared_task
def async_regenerate_qr(ad_id):
    ad = RealEstateAd.objects.get(pk=ad_id)
    ad.regenerate_qr_code()