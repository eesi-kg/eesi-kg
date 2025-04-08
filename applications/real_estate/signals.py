from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver
from .models import RealEstateAdImage, RealEstateAd
import cloudinary.uploader
from applications.user.tasks import send_approval_email


@receiver(pre_save, sender=RealEstateAdImage)
def handle_main_image(sender, instance, **kwargs):
    if instance.is_main:
        RealEstateAdImage.objects.filter(
            ad=instance.ad,
            is_main=True
        ).exclude(pk=instance.pk).update(is_main=False)


@receiver(post_delete, sender=RealEstateAdImage)
def delete_cloudinary_image(sender, instance, **kwargs):
    try:
        cloudinary.uploader.destroy(instance.image.public_id)
    except Exception as e:
        print(f"Error deleting image: {e}")

    if instance.is_main:
        next_image = RealEstateAdImage.objects.filter(
            ad=instance.ad
        ).first()
        if next_image:
            next_image.is_main = True
            next_image.save()


@receiver(post_delete, sender=RealEstateAd)
def delete_associated_files(sender, instance, **kwargs):
    # Delete QR code
    if instance.qr_code:
        try:
            cloudinary.uploader.destroy(instance.qr_code.public_id)
        except:
            pass

    # Delete documents
    for field in [instance.measurements_docs, instance.designing_docs]:
        if field:
            try:
                cloudinary.uploader.destroy(field.public_id, resource_type="raw")
            except:
                pass


@receiver(post_save, sender=RealEstateAd)
def notify_on_approval(sender, instance, **kwargs):
    update_fields = kwargs.get('update_fields', None)
    if instance.is_approved and update_fields and 'is_approved' in update_fields:
        send_approval_email.delay(instance.user.email, instance.public_id)