from celery import shared_task
from django.utils.timezone import now
from datetime import timedelta

from .models import ApartmentAd, HouseAd, CommercialAd, RoomAd, PlotAd, DachaAd, ParkingAd


@shared_task
def deactivate_expired_ads():
    ad_models = [ApartmentAd, HouseAd, CommercialAd, RoomAd, PlotAd, DachaAd, ParkingAd]
    total_deactivated = 0

    for model in ad_models:
        ads = model.objects.filter(is_active=True, subscription__isnull=False)

        for ad in ads:
            if ad.created_at and ad.subscription:
                expiration_date = ad.created_at + timedelta(days=ad.subscription.duration_days)
                if now() > expiration_date:
                    ad.is_active = False
                    ad.save(update_fields=['is_active'])
                    total_deactivated += 1

    return f"{total_deactivated} объявлений деактивировано."
