from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User, Profile, UserType


class CustomUserCreationForm(UserCreationForm):
    """Formulario de registro personalizado"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'tu@email.com'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Apellido'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'nombre_usuario'
        })
    )
    user_type = forms.ChoiceField(
        choices=[
            (UserType.BUYER, 'Comprador'),
            (UserType.SELLER, 'Vendedor/Creador')
        ],
        required=True,
        widget=forms.Select(attrs={
            'class': 'select select-bordered w-full'
        }),
        label='Tipo de cuenta'
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': '+54 11 1234-5678'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Contraseña'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Confirmar contraseña'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'phone', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Ya existe un usuario con este email.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nombre de usuario ya está en uso.')
        return username
    
    def clean_user_type(self):
        """Validar que no se pueda seleccionar administrador"""
        user_type = self.cleaned_data.get('user_type')
        if user_type == UserType.ADMIN:
            raise ValidationError('No puedes registrarte como administrador. Los permisos de administrador son asignados por el personal autorizado.')
        return user_type
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.user_type = self.cleaned_data['user_type']
        user.phone = self.cleaned_data['phone']
        
        if commit:
            user.save()
            # Crear perfil automáticamente
            Profile.objects.create(user=user)
        
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Formulario de login personalizado que usa email"""
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Correo electrónico',
            'autofocus': True
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Contraseña'
        })
    )
    
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            # Verificar que existe un usuario con este email
            try:
                user = User.objects.get(email=email)
                # Sobrescribir el username con el email para la autenticación
                self.cleaned_data['username'] = email
            except User.DoesNotExist:
                raise ValidationError('No existe un usuario con este email.')
        
        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    """Formulario para editar el perfil"""
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'birth_date', 'country', 'city', 'website', 'artist_name', 'genres']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 4,
                'placeholder': 'Cuéntanos sobre ti...'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'input input-bordered w-full',
                'type': 'date'
            }),
            'country': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'País'
            }),
            'city': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Ciudad'
            }),
            'website': forms.URLInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'https://tu-sitio-web.com'
            }),
            'artist_name': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Tu nombre artístico'
            }),
            'genres': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Rock, Pop, Jazz (separar con comas)'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'file-input file-input-bordered w-full'
            })
        }
