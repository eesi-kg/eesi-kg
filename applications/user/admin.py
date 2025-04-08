from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('full_name', 'phone_number')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('-date_joined',)
    search_fields = ('email', 'full_name')
    list_display_links = ('email', 'full_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_company:
            return qs.filter(user=request.user)
        return qs

    def has_change_permission(self, request, obj=None):
        if obj and request.user.is_company and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)