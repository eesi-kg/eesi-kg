from celery import shared_task

from applications.real_estate.models import RealEstateAd


@shared_task
def async_regenerate_qr(ad_id):
    ad = RealEstateAd.objects.get(pk=ad_id)
    ad.regenerate_qr_code()

    

@shared_task
def process_real_estate_images(ad_id):
    ad = RealEstateAd.objects.get(public_id=ad_id)
    for image in ad.images.all():
        optimize_image.delay(image.id)

@shared_task
def optimize_image(image_id):
    from PIL import Image
    image = RealEstateAdImage.objects.get(id=image_id)      