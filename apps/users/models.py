from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserType(models.TextChoices):
    """Tipos de usuarios en el marketplace de audios"""
    BUYER = 'buyer', 'Comprador'
    SELLER = 'seller', 'Vendedor/Creador' 
    ADMIN = 'admin', 'Administrador'


class User(AbstractUser):
    """Usuario personalizado para el marketplace de audios"""
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.BUYER,
        verbose_name='Tipo de usuario'
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Formato de teléfono inválido')],
        verbose_name='Teléfono'
    )
    is_verified = models.BooleanField(default=False, verbose_name='Usuario verificado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_user_type_display()})"
    
    def get_user_type_display(self):
        """Retorna la etiqueta legible del tipo de usuario"""
        return dict(UserType.choices).get(self.user_type, self.user_type)
    
    @property
    def is_buyer(self):
        return self.user_type == UserType.BUYER
    
    @property
    def is_seller(self):
        return self.user_type == UserType.SELLER
    
    @property
    def is_admin_user(self):
        return self.user_type == UserType.ADMIN or self.is_staff


class Profile(models.Model):
    """Perfil extendido del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Biografía'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de nacimiento'
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='País'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ciudad'
    )
    website = models.URLField(
        blank=True,
        verbose_name='Sitio web'
    )
    
    # Campos específicos para vendedores
    artist_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Nombre artístico'
    )
    genres = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Géneros musicales',
        help_text='Separar con comas'
    )
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
    
    def __str__(self):
        return f"Perfil de {self.user.get_full_name()}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea automáticamente un perfil cuando se crea un usuario"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Guarda el perfil cuando se guarda el usuario"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
