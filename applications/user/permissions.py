from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from rest_framework import permissions

from applications.real_estate.models import RealEstateAd


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsModeratorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_moderator


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


def add_custom_permissions(sender, **kwargs):
    Permission.objects.get_or_create(
        codename='can_approve_ads',
        name='Can approve ads',
        content_type=ContentType.objects.get_for_model(RealEstateAd)
    )


post_migrate.connect(add_custom_permissions)
