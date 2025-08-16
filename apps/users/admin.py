from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Perfil'
    verbose_name_plural = 'Perfil'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Administración personalizada de usuarios"""
    inlines = (ProfileInline,)
    list_display = ('email', 'username', 'first_name', 'last_name', 'user_type', 'is_verified', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('user_type', 'phone', 'is_verified')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Adicional', {
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'phone')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Administración de perfiles"""
    list_display = ('user', 'country', 'city', 'artist_name')
    list_filter = ('country', 'user__user_type')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'artist_name')
    readonly_fields = ('user',)
