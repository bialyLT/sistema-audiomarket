from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from functools import wraps
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileForm
from .models import User


def redirect_authenticated_users(view_func):
    """
    Decorador que redirige usuarios autenticados a su dashboard correspondiente
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Ya tienes una sesión iniciada.')
            if request.user.is_admin_user:
                return redirect('users:dashboard_admin')
            elif request.user.is_seller:
                return redirect('users:dashboard_seller')
            else:
                return redirect('users:dashboard_buyer')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


class RegisterView(CreateView):
    """Vista de registro de usuarios"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def dispatch(self, request, *args, **kwargs):
        """Redirigir usuarios autenticados lejos del registro"""
        if request.user.is_authenticated:
            messages.info(request, 'Ya tienes una sesión iniciada.')
            # Redirigir según el tipo de usuario
            if request.user.is_admin_user:
                return redirect('users:dashboard_admin')
            elif request.user.is_seller:
                return redirect('users:dashboard_seller')
            else:
                return redirect('users:dashboard_buyer')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request, 
            f'¡Cuenta creada exitosamente! Bienvenido al marketplace de audios.'
        )
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Por favor corrige los errores en el formulario.'
        )
        return super().form_invalid(form)


# Vista alternativa basada en función para el registro (opcional)
@redirect_authenticated_users  
def register_view(request):
    """Vista de registro basada en función como alternativa"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                f'¡Cuenta creada exitosamente! Bienvenido al marketplace de audios, {user.first_name}.'
            )
            return redirect('users:login')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@redirect_authenticated_users
def custom_login_view(request):
    """Vista de login personalizada usando email como identificador"""    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # Es el email
            password = form.cleaned_data.get('password')
            
            # Autenticar usando email directamente
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'¡Bienvenido de nuevo, {user.first_name}!')
                
                # Redirección basada en tipo de usuario
                if user.is_admin_user:
                    return redirect('users:dashboard_admin')
                elif user.is_seller:
                    return redirect('users:dashboard_seller')
                else:
                    return redirect('users:dashboard_buyer')
            else:
                messages.error(request, 'Email o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile_view(request):
    """Vista del perfil de usuario"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProfileForm(instance=profile)
    
    context = {
        'form': form,
        'user': request.user,
        'profile': profile
    }
    return render(request, 'users/profile.html', context)


@login_required
def dashboard_buyer(request):
    """Dashboard para compradores"""
    if not request.user.is_buyer and not request.user.is_admin_user:
        messages.warning(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('core:home')
    
    context = {
        'user': request.user,
        'user_type': 'buyer'
    }
    return render(request, 'users/dashboard_buyer.html', context)


@login_required
def dashboard_seller(request):
    """Dashboard para vendedores/creadores"""
    if not request.user.is_seller and not request.user.is_admin_user:
        messages.warning(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('core:home')
    
    # Importar el modelo Audio
    from apps.audios.models import Audio
    
    # Obtener audios del vendedor
    user_audios = Audio.objects.filter(seller=request.user).order_by('-created_at')
    
    # Estadísticas del vendedor
    stats = {
        'total_audios': user_audios.count(),
        'published_audios': user_audios.filter(status=Audio.Status.PUBLISHED).count(),
        'pending_audios': user_audios.filter(status=Audio.Status.PENDING).count(),
        'draft_audios': user_audios.filter(status=Audio.Status.DRAFT).count(),
        'total_views': sum(audio.views_count for audio in user_audios),
        'total_downloads': sum(audio.downloads_count for audio in user_audios),
        'total_favorites': sum(audio.favorites_count for audio in user_audios),
    }
    
    # Calcular ganancias (por ahora 0, se implementará con el sistema de pagos)
    stats['total_sales'] = 0
    stats['monthly_sales'] = 0
    
    # Audios recientes (últimos 5)
    recent_audios = user_audios[:5]
    
    context = {
        'user': request.user,
        'user_type': 'seller',
        'stats': stats,
        'recent_audios': recent_audios,
    }
    return render(request, 'users/dashboard_seller.html', context)


@login_required
def dashboard_admin(request):
    """Dashboard para administradores"""
    if not request.user.is_admin_user:
        messages.warning(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('core:home')
    
    # Estadísticas básicas
    total_users = User.objects.count()
    buyers = User.objects.filter(user_type='buyer').count()
    sellers = User.objects.filter(user_type='seller').count()
    admins = User.objects.filter(user_type='admin').count()
    
    context = {
        'user': request.user,
        'user_type': 'admin',
        'stats': {
            'total_users': total_users,
            'buyers': buyers,
            'sellers': sellers,
            'admins': admins
        }
    }
    return render(request, 'users/dashboard_admin.html', context)
