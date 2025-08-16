import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()


def audio_upload_path(instance, filename):
    """Genera la ruta donde se guardará el archivo de audio"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('audios', str(instance.seller.id), filename)


def cover_upload_path(instance, filename):
    """Genera la ruta donde se guardará la imagen de portada"""
    ext = filename.split('.')[-1]
    filename = f"cover_{uuid.uuid4()}.{ext}"
    return os.path.join('covers', str(instance.seller.id), filename)


class Category(models.Model):
    """Categorías de audios (Música, Efectos de sonido, etc.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    description = models.TextField(blank=True, verbose_name='Descripción')
    icon = models.CharField(max_length=50, blank=True, verbose_name='Icono CSS', 
                           help_text='Clase CSS del icono (ej: fas fa-music)')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Genre(models.Model):
    """Géneros musicales"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='genres', verbose_name='Categoría')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    class Meta:
        verbose_name = 'Género'
        verbose_name_plural = 'Géneros'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Etiquetas para clasificación adicional de audios"""
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')
    color = models.CharField(max_length=7, default='#3B82F6', verbose_name='Color', 
                            help_text='Color en formato hexadecimal')
    
    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Audio(models.Model):
    """Modelo principal para los audios en el marketplace"""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Borrador'
        PENDING = 'pending', 'Pendiente de revisión'
        PUBLISHED = 'published', 'Publicado'
        REJECTED = 'rejected', 'Rechazado'
        INACTIVE = 'inactive', 'Inactivo'
    
    class License(models.TextChoices):
        STANDARD = 'standard', 'Licencia Estándar'
        EXTENDED = 'extended', 'Licencia Extendida'
        EXCLUSIVE = 'exclusive', 'Licencia Exclusiva'
    
    # Información básica
    title = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Descripción')
    
    # Relaciones
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audios_for_sale', 
                              verbose_name='Vendedor')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='audios', 
                                verbose_name='Categoría')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='audios', 
                             verbose_name='Género')
    tags = models.ManyToManyField(Tag, blank=True, related_name='audios', verbose_name='Etiquetas')
    
    # Archivos
    audio_file = models.FileField(
        upload_to=audio_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'flac', 'aac', 'ogg'])],
        verbose_name='Archivo de Audio'
    )
    cover_image = models.ImageField(
        upload_to=cover_upload_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        verbose_name='Imagen de Portada'
    )
    
    # Información técnica
    duration = models.DurationField(blank=True, null=True, verbose_name='Duración')
    file_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='Tamaño del archivo (bytes)')
    bitrate = models.PositiveIntegerField(blank=True, null=True, verbose_name='Bitrate (kbps)')
    sample_rate = models.PositiveIntegerField(blank=True, null=True, verbose_name='Sample Rate (Hz)')
    
    # Precios y licencias
    price_standard = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        verbose_name='Precio Licencia Estándar'
    )
    price_extended = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        blank=True, 
        null=True,
        verbose_name='Precio Licencia Extendida'
    )
    price_exclusive = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)],
        blank=True, 
        null=True,
        verbose_name='Precio Licencia Exclusiva'
    )
    
    # Estado y metadata
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, 
                             verbose_name='Estado')
    is_featured = models.BooleanField(default=False, verbose_name='Destacado')
    allow_preview = models.BooleanField(default=True, verbose_name='Permitir vista previa')
    
    # Estadísticas
    views_count = models.PositiveIntegerField(default=0, verbose_name='Visualizaciones')
    downloads_count = models.PositiveIntegerField(default=0, verbose_name='Descargas')
    favorites_count = models.PositiveIntegerField(default=0, verbose_name='Favoritos')
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de publicación')
    
    class Meta:
        verbose_name = 'Audio'
        verbose_name_plural = 'Audios'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['-published_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.seller.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid.uuid4().hex[:8]}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('audios:detail', kwargs={'slug': self.slug})
    
    @property
    def is_published(self):
        return self.status == self.Status.PUBLISHED
    
    @property
    def file_size_mb(self):
        """Retorna el tamaño del archivo en MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return None
    
    def get_price_for_license(self, license_type):
        """Obtiene el precio para un tipo de licencia específico"""
        price_mapping = {
            self.License.STANDARD: self.price_standard,
            self.License.EXTENDED: self.price_extended,
            self.License.EXCLUSIVE: self.price_exclusive,
        }
        return price_mapping.get(license_type)


class AudioFavorite(models.Model):
    """Audios marcados como favoritos por los usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_audios')
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Favorito'
        verbose_name_plural = 'Favoritos'
        unique_together = ('user', 'audio')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.audio.title}"


class AudioReview(models.Model):
    """Reseñas y calificaciones de audios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audio_reviews')
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Calificación'
    )
    comment = models.TextField(blank=True, verbose_name='Comentario')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        unique_together = ('user', 'audio')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.audio.title} ({self.rating}★)"


class AudioPlaylist(models.Model):
    """Playlists de audios creadas por usuarios"""
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    audios = models.ManyToManyField(Audio, blank=True, related_name='in_playlists')
    is_public = models.BooleanField(default=False, verbose_name='Pública')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.get_full_name()}"
    
    @property
    def total_duration(self):
        """Duración total de la playlist"""
        from django.db.models import Sum
        from datetime import timedelta
        
        total = self.audios.aggregate(
            total_duration=Sum('duration')
        )['total_duration']
        
        return total or timedelta(seconds=0)
