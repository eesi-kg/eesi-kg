from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import VehicleImage, VehicleAd
import cloudinary.uploader


@receiver(pre_save, sender=VehicleImage)
def handle_main_image(sender, instance, **kwargs):
    if instance.is_main:
        VehicleImage.objects.filter(
            vehicle=instance.vehicle,
            is_main=True
        ).exclude(pk=instance.pk).update(is_main=False)


@receiver(post_delete, sender=VehicleImage)
def delete_cloudinary_image(sender, instance, **kwargs):
    try:
        cloudinary.uploader.destroy(instance.image.public_id)
    except:
        pass

    if instance.is_main:
        next_image = VehicleImage.objects.filter(
            vehicle=instance.vehicle
        ).first()
        if next_image:
            next_image.is_main = True
            next_image.save()


@receiver(post_delete, sender=VehicleAd)
def delete_associated_files(sender, instance, **kwargs):
    if instance.qr_code:
        try:
            cloudinary.uploader.destroy(instance.qr_code.public_id)
        except:
            pass
