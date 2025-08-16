from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Avg
from django.contrib import messages

from .models import (
    Category, Genre, Tag, Audio, AudioFavorite, 
    AudioReview, AudioPlaylist
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'audio_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    actions = ['activate_categories', 'deactivate_categories']
    
    def audio_count(self, obj):
        count = obj.audios.filter(status=Audio.Status.PUBLISHED).count()
        return format_html(
            '<span class="badge badge-info">{}</span>',
            count
        )
    audio_count.short_description = 'Audios'
    
    def activate_categories(self, request, queryset):
        updated = queryset.update(is_active=True)
        messages.success(request, f'{updated} categoría(s) activada(s).')
    activate_categories.short_description = "✅ Activar categorías seleccionadas"
    
    def deactivate_categories(self, request, queryset):
        updated = queryset.update(is_active=False)
        messages.success(request, f'{updated} categoría(s) desactivada(s).')
    deactivate_categories.short_description = "❌ Desactivar categorías seleccionadas"


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'audio_count', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    
    def audio_count(self, obj):
        count = obj.audios.filter(status=Audio.Status.PUBLISHED).count()
        return format_html(
            '<span class="badge badge-secondary">{}</span>',
            count
        )
    audio_count.short_description = 'Audios'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_preview', 'audio_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    
    def color_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 2px 8px; border-radius: 4px; color: white;">{}</span>',
            obj.color,
            obj.name
        )
    color_preview.short_description = 'Color'
    
    def audio_count(self, obj):
        count = obj.audios.filter(status=Audio.Status.PUBLISHED).count()
        return format_html(
            '<span class="badge badge-warning">{}</span>',
            count
        )
    audio_count.short_description = 'Audios'


class AudioReviewInline(admin.TabularInline):
    model = AudioReview
    extra = 0
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    can_delete = True
    
    def has_add_permission(self, request, obj):
        return False


@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'seller', 'category', 'status', 'price_standard',
        'views_count', 'downloads_count', 'is_featured', 'created_at'
    )
    list_filter = (
        'status', 'category', 'genre', 'is_featured', 
        'allow_preview', 'created_at', 'published_at'
    )
    search_fields = ('title', 'description', 'seller__email', 'seller__first_name', 'seller__last_name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = (
        'slug', 'views_count', 'downloads_count', 'favorites_count',
        'file_size', 'duration', 'bitrate', 'sample_rate',
        'created_at', 'updated_at', 'published_at'
    )
    actions = [
        'publish_audios', 'unpublish_audios', 'feature_audios', 
        'unfeature_audios', 'reject_audios'
    ]
    inlines = [AudioReviewInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'description', 'seller')
        }),
        ('Clasificación', {
            'fields': ('category', 'genre', 'tags')
        }),
        ('Archivos', {
            'fields': ('audio_file', 'cover_image', 'cover_preview')
        }),
        ('Información Técnica', {
            'fields': ('duration', 'file_size', 'bitrate', 'sample_rate'),
            'classes': ('collapse',)
        }),
        ('Precios', {
            'fields': ('price_standard', 'price_extended', 'price_exclusive')
        }),
        ('Estado y Configuración', {
            'fields': ('status', 'is_featured', 'allow_preview')
        }),
        ('Estadísticas', {
            'fields': ('views_count', 'downloads_count', 'favorites_count'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 200px;" />',
                obj.cover_image.url
            )
        return "Sin imagen"
    cover_preview.short_description = 'Vista previa'
    
    def publish_audios(self, request, queryset):
        updated = queryset.update(status=Audio.Status.PUBLISHED)
        messages.success(request, f'{updated} audio(s) publicado(s).')
    publish_audios.short_description = "📢 Publicar audios seleccionados"
    
    def unpublish_audios(self, request, queryset):
        updated = queryset.update(status=Audio.Status.DRAFT)
        messages.success(request, f'{updated} audio(s) despublicado(s).')
    unpublish_audios.short_description = "📝 Despublicar audios seleccionados"
    
    def feature_audios(self, request, queryset):
        updated = queryset.update(is_featured=True)
        messages.success(request, f'{updated} audio(s) destacado(s).')
    feature_audios.short_description = "⭐ Destacar audios seleccionados"
    
    def unfeature_audios(self, request, queryset):
        updated = queryset.update(is_featured=False)
        messages.success(request, f'{updated} audio(s) quitado(s) de destacados.')
    unfeature_audios.short_description = "⭐ Quitar de destacados"
    
    def reject_audios(self, request, queryset):
        updated = queryset.update(status=Audio.Status.REJECTED)
        messages.success(request, f'{updated} audio(s) rechazado(s).')
    reject_audios.short_description = "❌ Rechazar audios seleccionados"


@admin.register(AudioFavorite)
class AudioFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio', 'created_at')
    list_filter = ('created_at', 'audio__category')
    search_fields = ('user__email', 'audio__title')
    readonly_fields = ('user', 'audio', 'created_at')
    
    def has_add_permission(self, request):
        return False


@admin.register(AudioReview)
class AudioReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'audio', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'audio__category')
    search_fields = ('user__email', 'audio__title', 'comment')
    readonly_fields = ('user', 'audio', 'created_at', 'updated_at')
    
    def has_add_permission(self, request):
        return False


@admin.register(AudioPlaylist)
class AudioPlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'audio_count', 'is_public', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'user__email', 'description')
    filter_horizontal = ('audios',)
    
    def audio_count(self, obj):
        count = obj.audios.count()
        return format_html(
            '<span class="badge badge-primary">{}</span>',
            count
        )
    audio_count.short_description = 'Audios'


# Configuración del admin site
admin.site.site_header = "AudioMarket - Administración"
admin.site.site_title = "AudioMarket Admin"
admin.site.index_title = "Panel de Administración"
