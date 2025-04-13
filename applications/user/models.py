from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _


class UserRole(models.TextChoices):
    CUSTOMER = 'CUSTOMER', _('Клиент')
    MODERATOR = 'MODERATOR', _('Модератор')
    ADMIN = 'ADMIN', _('Администратор')
    COMPANY = 'COMPANY', _('Компания')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRole.CUSTOMER)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', UserRole.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def create_moderator(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', UserRole.MODERATOR)
        return self._create_user(email, password, **extra_fields)

    def create_company(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_company', True)
        extra_fields.setdefault('role', UserRole.COMPANY)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email почта', unique=True, primary_key=True)
    role = models.CharField(
        'роль',
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER
    )
    is_active = models.BooleanField('активный', default=True)
    is_staff = models.BooleanField('статус администратора', default=False)
    is_company = models.BooleanField('статус компании', default=False)
    date_joined = models.DateTimeField('время присоеденения', default=timezone.now)

    activation_code = models.CharField('код активации', max_length=6, blank=True)
    full_name = models.CharField('имя', max_length=150, blank=True)
    phone_number = models.CharField('номер телефона', max_length=20, blank=True)
    reset_code = models.CharField(max_length=6, blank=True, null=True)
    reset_code_created_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = "пользователи"
        ordering = ('-date_joined',)

    def __str__(self):
        return f'{self.email} ({self.role})'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def generate_activation_code(self):
        code = get_random_string(6, '0123456789')
        self.activation_code = code
        self.save(update_fields=['activation_code'])
        return code

    def send_activation_email(self):
        from .tasks import send_activation_email_task
        send_activation_email_task.delay(self.pk)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_company_(self):
        return self.role == UserRole.COMPANY

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_superuser

    def generate_reset_code(self):
        self.reset_code = get_random_string(6, '0123456789')
        self.reset_code_created_at = timezone.now()
        self.save(update_fields=['reset_code', 'reset_code_created_at'])

    def send_password_reset_email(self):
        from .tasks import send_password_reset_email_task
        send_password_reset_email_task.delay(self.pk)
