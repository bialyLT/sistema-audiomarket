from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib import messages
from .models import User, Profile, UserType


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
    actions = ['promote_to_admin', 'demote_to_buyer', 'demote_to_seller']
    
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
    
    def promote_to_admin(self, request, queryset):
        """Promover usuarios seleccionados a administradores"""
        promoted_count = 0
        for user in queryset:
            if user.user_type != UserType.ADMIN:
                user.user_type = UserType.ADMIN
                user.is_staff = True
                user.save()
                promoted_count += 1
        
        if promoted_count > 0:
            messages.success(
                request, 
                f'{promoted_count} usuario(s) promovido(s) a administrador exitosamente.'
            )
        else:
            messages.info(request, 'No se encontraron usuarios para promover.')
    
    promote_to_admin.short_description = "🔝 Promover a administrador"
    
    def demote_to_buyer(self, request, queryset):
        """Degradar usuarios seleccionados a compradores"""
        demoted_count = 0
        for user in queryset:
            if user.user_type == UserType.ADMIN and not user.is_superuser:
                user.user_type = UserType.BUYER
                user.is_staff = False
                user.save()
                demoted_count += 1
        
        if demoted_count > 0:
            messages.success(
                request, 
                f'{demoted_count} usuario(s) degradado(s) a comprador exitosamente.'
            )
        else:
            messages.info(request, 'No se encontraron administradores para degradar (no se pueden degradar superusuarios).')
    
    demote_to_buyer.short_description = "🔽 Degradar a comprador"
    
    def demote_to_seller(self, request, queryset):
        """Cambiar usuarios seleccionados a vendedores"""
        changed_count = 0
        for user in queryset:
            if user.user_type != UserType.SELLER:
                user.user_type = UserType.SELLER
                if user.user_type == UserType.ADMIN and not user.is_superuser:
                    user.is_staff = False
                user.save()
                changed_count += 1
        
        if changed_count > 0:
            messages.success(
                request, 
                f'{changed_count} usuario(s) cambiado(s) a vendedor exitosamente.'
            )
        else:
            messages.info(request, 'No se encontraron usuarios para cambiar.')
    
    demote_to_seller.short_description = "🎵 Cambiar a vendedor"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Administración de perfiles"""
    list_display = ('user', 'country', 'city', 'artist_name')
    list_filter = ('country', 'user__user_type')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'artist_name')
    readonly_fields = ('user',)
