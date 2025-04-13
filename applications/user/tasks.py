from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def send_activation_email_task(self, user_id):
    try:
        user = User.objects.get(pk=user_id)
        subject = 'Активация аккаунта'
        message = f'Ваш код активации: {user.activation_code}'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        logger.info(f"Письмо активации отправлено на {user.email}")

    except User.DoesNotExist:
        logger.error(f"Пользователь с ID {user_id} не найден")
    except Exception as exc:
        logger.error(f'Ошибка отправки письма: {exc}')
        self.retry(exc=exc, countdown=60)


@shared_task(bind=True, max_retries=3)
def send_password_reset_email_task(self, user_id):
    try:
        user = User.objects.get(pk=user_id)
        subject = 'Сброс пароля'
        message = f'Ваш код сброса пароля: {user.reset_code}'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        logger.info(f"Письмо сброса пароля отправлено на {user.email}")

    except User.DoesNotExist:
        logger.error(f"Пользователь с ID {user_id} не найден")
    except Exception as exc:
        logger.error(f'Ошибка отправки письма: {exc}')
        self.retry(exc=exc, countdown=60)



@shared_task
def send_approval_email(user_email, public_id):
    send_mail(
        'Ваше объявление одобрено',
        f'Объявление {public_id} теперь активно',
        'noreply@yourdomain.com',
        [user_email],
        fail_silently=True,
    )