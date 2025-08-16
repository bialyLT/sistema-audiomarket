import os
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from mutagen import File
from mutagen.id3 import ID3NoHeaderError
from PIL import Image
from .models import Audio, AudioFavorite


@receiver(pre_save, sender=Audio)
def extract_audio_metadata(sender, instance, **kwargs):
    """Extrae automáticamente metadata del archivo de audio"""
    if instance.audio_file:
        try:
            # Obtener información del archivo usando mutagen
            audio_file = File(instance.audio_file.file.name)
            if audio_file is not None:
                # Duración
                if audio_file.info.length:
                    instance.duration = timezone.timedelta(seconds=int(audio_file.info.length))
                
                # Bitrate
                if hasattr(audio_file.info, 'bitrate') and audio_file.info.bitrate:
                    instance.bitrate = audio_file.info.bitrate
                
                # Sample rate
                if hasattr(audio_file.info, 'sample_rate'):
                    instance.sample_rate = audio_file.info.sample_rate
                elif hasattr(audio_file.info, 'samplerate'):
                    instance.sample_rate = audio_file.info.samplerate
            
            # Tamaño del archivo
            instance.file_size = instance.audio_file.size
            
        except (ID3NoHeaderError, Exception) as e:
            # Si no se puede leer la metadata, continuar sin error
            print(f"No se pudo extraer metadata del audio {instance.title}: {e}")


@receiver(pre_save, sender=Audio)
def optimize_cover_image(sender, instance, **kwargs):
    """Optimiza la imagen de portada si es necesaria"""
    if instance.cover_image:
        try:
            # Abrir la imagen
            img = Image.open(instance.cover_image.file)
            
            # Convertir a RGB si es necesario
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Redimensionar si es muy grande (máximo 800x800)
            max_size = (800, 800)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Guardar la imagen optimizada
                img.save(instance.cover_image.file.name, 'JPEG', quality=85, optimize=True)
                
        except Exception as e:
            print(f"No se pudo optimizar la imagen de portada para {instance.title}: {e}")


@receiver(post_save, sender=Audio)
def update_published_at(sender, instance, **kwargs):
    """Actualiza la fecha de publicación cuando el estado cambia a publicado"""
    if instance.status == Audio.Status.PUBLISHED and not instance.published_at:
        Audio.objects.filter(id=instance.id).update(published_at=timezone.now())


@receiver(post_save, sender=AudioFavorite)
def update_favorites_count_add(sender, instance, created, **kwargs):
    """Incrementa el contador de favoritos cuando se agrega un favorito"""
    if created:
        instance.audio.favorites_count += 1
        instance.audio.save(update_fields=['favorites_count'])


@receiver(post_delete, sender=AudioFavorite)
def update_favorites_count_remove(sender, instance, **kwargs):
    """Decrementa el contador de favoritos cuando se elimina un favorito"""
    instance.audio.favorites_count = max(0, instance.audio.favorites_count - 1)
    instance.audio.save(update_fields=['favorites_count'])


@receiver(post_delete, sender=Audio)
def delete_audio_files(sender, instance, **kwargs):
    """Elimina los archivos físicos cuando se elimina un audio"""
    # Eliminar archivo de audio
    if instance.audio_file:
        if os.path.isfile(instance.audio_file.path):
            try:
                os.remove(instance.audio_file.path)
            except Exception as e:
                print(f"Error eliminando archivo de audio: {e}")
    
    # Eliminar imagen de portada
    if instance.cover_image:
        if os.path.isfile(instance.cover_image.path):
            try:
                os.remove(instance.cover_image.path)
            except Exception as e:
                print(f"Error eliminando imagen de portada: {e}")


# Signal para limpiar archivos cuando se actualiza el audio
@receiver(pre_save, sender=Audio)
def delete_old_files_on_update(sender, instance, **kwargs):
    """Elimina archivos antiguos cuando se actualizan"""
    if not instance.pk:
        return
    
    try:
        old_audio = Audio.objects.get(pk=instance.pk)
    except Audio.DoesNotExist:
        return
    
    # Eliminar archivo de audio antiguo si cambió
    if old_audio.audio_file and old_audio.audio_file != instance.audio_file:
        if os.path.isfile(old_audio.audio_file.path):
            try:
                os.remove(old_audio.audio_file.path)
            except Exception as e:
                print(f"Error eliminando archivo de audio antiguo: {e}")
    
    # Eliminar imagen de portada antigua si cambió
    if old_audio.cover_image and old_audio.cover_image != instance.cover_image:
        if os.path.isfile(old_audio.cover_image.path):
            try:
                os.remove(old_audio.cover_image.path)
            except Exception as e:
                print(f"Error eliminando imagen de portada antigua: {e}")
