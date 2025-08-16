from django import forms
from django.core.exceptions import ValidationError
from .models import Audio, Category, Genre, Tag, AudioReview, AudioPlaylist


class AudioUploadForm(forms.ModelForm):
    """Formulario para subir/editar audios"""
    
    # Campo adicional para estado inicial
    initial_status = forms.ChoiceField(
        choices=[
            (Audio.Status.DRAFT, 'Guardar como borrador'),
            (Audio.Status.PENDING, 'Enviar para revisión'),
            (Audio.Status.PUBLISHED, 'Publicar inmediatamente'),
        ],
        initial=Audio.Status.DRAFT,
        widget=forms.RadioSelect(attrs={'class': 'radio-group'}),
        label='¿Qué quieres hacer con este audio?',
        help_text='Los borradores solo son visibles para ti. Los audios enviados para revisión serán evaluados por moderadores.'
    )
    
    class Meta:
        model = Audio
        fields = [
            'title', 'description', 'category', 'genre', 'tags',
            'audio_file', 'cover_image', 'price_standard', 
            'price_extended', 'price_exclusive', 'allow_preview'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Título del audio'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4,
                'placeholder': 'Describe tu audio, su uso recomendado, instrumentos utilizados, etc.'
            }),
            'category': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),
            'genre': forms.Select(attrs={
                'class': 'select select-bordered w-full',
            }),
            'tags': forms.CheckboxSelectMultiple(attrs={
                'class': 'checkbox-group'
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered w-full',
                'accept': '.mp3,.wav,.flac,.aac,.ogg'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered w-full',
                'accept': '.jpg,.jpeg,.png,.webp'
            }),
            'price_standard': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'price_extended': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '0.00 (opcional)',
                'step': '0.01',
                'min': '0.01'
            }),
            'price_exclusive': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '0.00 (opcional)',
                'step': '0.01',
                'min': '0.01'
            }),
            'allow_preview': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar géneros activos
        self.fields['genre'].queryset = Genre.objects.filter(is_active=True)
        
        # Filtrar categorías activas
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        
        # Solo tags activos (si implementas is_active en Tag)
        # self.fields['tags'].queryset = Tag.objects.filter(is_active=True)
        
    def clean_audio_file(self):
        audio_file = self.cleaned_data.get('audio_file')
        if audio_file:
            # Validar tamaño máximo (50MB)
            if audio_file.size > 50 * 1024 * 1024:
                raise ValidationError('El archivo de audio no puede superar los 50MB.')
            
            # Validar extensión
            allowed_extensions = ['mp3', 'wav', 'flac', 'aac', 'ogg']
            extension = audio_file.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError(f'Formato no permitido. Use: {", ".join(allowed_extensions)}')
        
        return audio_file
    
    def clean_cover_image(self):
        cover_image = self.cleaned_data.get('cover_image')
        if cover_image:
            # Validar tamaño máximo (5MB)
            if cover_image.size > 5 * 1024 * 1024:
                raise ValidationError('La imagen no puede superar los 5MB.')
            
            # Validar extensión
            allowed_extensions = ['jpg', 'jpeg', 'png', 'webp']
            extension = cover_image.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise ValidationError(f'Formato no permitido. Use: {", ".join(allowed_extensions)}')
        
        return cover_image
    
    def clean(self):
        cleaned_data = super().clean()
        price_standard = cleaned_data.get('price_standard')
        price_extended = cleaned_data.get('price_extended')
        price_exclusive = cleaned_data.get('price_exclusive')
        
        # Validar que los precios extended y exclusive sean mayores que standard
        if price_extended and price_standard:
            if price_extended <= price_standard:
                raise ValidationError({
                    'price_extended': 'El precio extendido debe ser mayor al precio estándar.'
                })
        
        if price_exclusive and price_standard:
            if price_exclusive <= price_standard:
                raise ValidationError({
                    'price_exclusive': 'El precio exclusivo debe ser mayor al precio estándar.'
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.seller = self.user
            
        # Establecer el estado basado en la selección del usuario
        if 'initial_status' in self.cleaned_data:
            instance.status = self.cleaned_data['initial_status']
            
            # Si se está publicando directamente, establecer fecha de publicación
            if instance.status == Audio.Status.PUBLISHED:
                from django.utils import timezone
                instance.published_at = timezone.now()
        
        if commit:
            instance.save()
            self.save_m2m()  # Guardar relaciones many-to-many
        return instance


class AudioFilterForm(forms.Form):
    """Formulario para filtrar audios"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Buscar audios...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label='Todas las categorías',
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.filter(is_active=True),
        required=False,
        empty_label='Todos los géneros',
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Precio mínimo',
            'step': '0.01'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Precio máximo',
            'step': '0.01'
        })
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Relevancia'),
            ('-published_at', 'Más recientes'),
            ('published_at', 'Más antiguos'),
            ('price_standard', 'Precio: menor a mayor'),
            ('-price_standard', 'Precio: mayor a menor'),
            ('-views_count', 'Más populares'),
            ('-downloads_count', 'Más descargados'),
            ('-favorites_count', 'Más favoritos'),
        ],
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        })
    )


class AudioReviewForm(forms.ModelForm):
    """Formulario para reseñas de audios"""
    
    class Meta:
        model = AudioReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} estrella{"s" if i > 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'select select-bordered w-full'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder': 'Escribe tu reseña (opcional)...'
            })
        }


class PlaylistForm(forms.ModelForm):
    """Formulario para crear/editar playlists"""
    
    class Meta:
        model = AudioPlaylist
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Nombre de la playlist'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder': 'Descripción de la playlist (opcional)'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            })
        }


class BulkActionForm(forms.Form):
    """Formulario para acciones masivas en audios"""
    ACTION_CHOICES = [
        ('publish', 'Publicar seleccionados'),
        ('unpublish', 'Despublicar seleccionados'),
        ('delete', 'Eliminar seleccionados'),
        ('feature', 'Marcar como destacados'),
        ('unfeature', 'Quitar destacado'),
    ]
    
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={
            'class': 'select select-bordered'
        })
    )
    selected_audios = forms.CharField(
        widget=forms.HiddenInput()
    )


class CategoryForm(forms.ModelForm):
    """Formulario para categorías (uso administrativo)"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
            'icon': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'fas fa-music'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            })
        }


class GenreForm(forms.ModelForm):
    """Formulario para géneros (uso administrativo)"""
    
    class Meta:
        model = Genre
        fields = ['name', 'category', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'category': forms.Select(attrs={
                'class': 'select select-bordered w-full'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'checkbox checkbox-primary'
            })
        }
