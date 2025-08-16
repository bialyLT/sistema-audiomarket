from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count
from django.http import JsonResponse, Http404, HttpResponseForbidden
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from django.db.models import F

from .models import Audio, Category, Genre, Tag, AudioFavorite, AudioReview, AudioPlaylist
from .forms import AudioUploadForm, AudioFilterForm, AudioReviewForm, PlaylistForm

User = get_user_model()


def audio_list(request):
    """Lista de audios con filtros y búsqueda"""
    form = AudioFilterForm(request.GET)
    audios = Audio.objects.filter(status=Audio.Status.PUBLISHED).select_related(
        'seller', 'category', 'genre'
    ).prefetch_related('tags')
    
    # Aplicar filtros
    if form.is_valid():
        search = form.cleaned_data.get('search')
        if search:
            audios = audios.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(seller__first_name__icontains=search) |
                Q(seller__last_name__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()
        
        category = form.cleaned_data.get('category')
        if category:
            audios = audios.filter(category=category)
        
        genre = form.cleaned_data.get('genre')
        if genre:
            audios = audios.filter(genre=genre)
        
        min_price = form.cleaned_data.get('min_price')
        if min_price:
            audios = audios.filter(price_standard__gte=min_price)
        
        max_price = form.cleaned_data.get('max_price')
        if max_price:
            audios = audios.filter(price_standard__lte=max_price)
        
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            audios = audios.order_by(sort_by)
    
    # Paginación
    paginator = Paginator(audios, 12)  # 12 audios por página
    page = request.GET.get('page')
    audios_page = paginator.get_page(page)
    
    # Estadísticas para la sidebar
    stats = {
        'total_audios': Audio.objects.filter(status=Audio.Status.PUBLISHED).count(),
        'categories': Category.objects.filter(is_active=True).annotate(
            audio_count=Count('audios', filter=Q(audios__status=Audio.Status.PUBLISHED))
        ),
        'featured_audios': Audio.objects.filter(
            status=Audio.Status.PUBLISHED, 
            is_featured=True
        )[:6]
    }
    
    context = {
        'audios': audios_page,
        'form': form,
        'stats': stats,
        'active_filters': any([
            form.cleaned_data.get('search') if form.is_valid() else False,
            form.cleaned_data.get('category') if form.is_valid() else False,
            form.cleaned_data.get('genre') if form.is_valid() else False,
            form.cleaned_data.get('min_price') if form.is_valid() else False,
            form.cleaned_data.get('max_price') if form.is_valid() else False,
        ])
    }
    
    return render(request, 'audios/list.html', context)


def audio_detail(request, slug):
    """Detalle de un audio específico"""
    audio = get_object_or_404(
        Audio.objects.select_related('seller', 'category', 'genre').prefetch_related('tags'),
        slug=slug,
        status=Audio.Status.PUBLISHED
    )
    
    # Incrementar contador de visualizaciones
    Audio.objects.filter(id=audio.id).update(views_count=F('views_count') + 1)
    
    # Verificar si está en favoritos (si el usuario está logueado)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = AudioFavorite.objects.filter(user=request.user, audio=audio).exists()
    
    # Obtener reseñas
    reviews = audio.reviews.select_related('user').order_by('-created_at')[:10]
    
    # Estadísticas de reseñas
    review_stats = audio.reviews.aggregate(
        avg_rating=Avg('rating'),
        total_reviews=Count('rating')
    )
    
    # Audios relacionados (mismo género, excluyendo el actual)
    related_audios = Audio.objects.filter(
        genre=audio.genre,
        status=Audio.Status.PUBLISHED
    ).exclude(id=audio.id).select_related('seller')[:6]
    
    # Más audios del mismo vendedor
    more_from_seller = Audio.objects.filter(
        seller=audio.seller,
        status=Audio.Status.PUBLISHED
    ).exclude(id=audio.id).select_related('category')[:4]
    
    context = {
        'audio': audio,
        'is_favorite': is_favorite,
        'reviews': reviews,
        'review_stats': review_stats,
        'related_audios': related_audios,
        'more_from_seller': more_from_seller,
        'can_review': request.user.is_authenticated and request.user != audio.seller,
    }
    
    return render(request, 'audios/detail.html', context)


@login_required
def audio_upload(request):
    """Subir nuevo audio"""
    if not request.user.is_seller and not request.user.is_admin_user:
        messages.error(request, 'Solo los vendedores pueden subir audios.')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            audio = form.save()
            messages.success(request, f'Audio "{audio.title}" subido exitosamente.')
            return redirect('audios:my_audios')
    else:
        form = AudioUploadForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Subir Nuevo Audio'
    }
    
    return render(request, 'audios/upload.html', context)


@login_required
def audio_edit(request, slug):
    """Editar audio existente"""
    audio = get_object_or_404(Audio, slug=slug, seller=request.user)
    
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES, instance=audio, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Audio "{audio.title}" actualizado exitosamente.')
            return redirect('audios:detail', slug=audio.slug)
    else:
        form = AudioUploadForm(instance=audio, user=request.user)
    
    context = {
        'form': form,
        'audio': audio,
        'title': f'Editar: {audio.title}'
    }
    
    return render(request, 'audios/upload.html', context)


@login_required
def my_audios(request):
    """Lista de audios del usuario logueado"""
    if not request.user.is_seller and not request.user.is_admin_user:
        messages.error(request, 'Solo los vendedores pueden acceder a esta sección.')
        return redirect('core:home')
    
    audios = Audio.objects.filter(seller=request.user).order_by('-created_at')
    
    # Filtro por estado
    status_filter = request.GET.get('status')
    if status_filter and status_filter in [choice[0] for choice in Audio.Status.choices]:
        audios = audios.filter(status=status_filter)
    
    # Filtro de ordenamiento
    sort_filter = request.GET.get('sort', 'newest')
    if sort_filter == 'oldest':
        audios = audios.order_by('created_at')
    elif sort_filter == 'title':
        audios = audios.order_by('title')
    elif sort_filter == 'views':
        audios = audios.order_by('-views_count')
    elif sort_filter == 'downloads':
        audios = audios.order_by('-downloads_count')
    # 'newest' es el default, ya está aplicado arriba
    
    # Estadísticas del vendedor
    stats = {
        'total': audios.count(),
        'published': audios.filter(status=Audio.Status.PUBLISHED).count(),
        'pending': audios.filter(status=Audio.Status.PENDING).count(),
        'draft': audios.filter(status=Audio.Status.DRAFT).count(),
        'total_views': sum(audio.views_count for audio in audios),
        'total_downloads': sum(audio.downloads_count for audio in audios),
    }
    
    # Paginación
    paginator = Paginator(audios, 10)
    page = request.GET.get('page')
    audios_page = paginator.get_page(page)
    
    context = {
        'audios': audios_page,
        'stats': stats
    }
    
    return render(request, 'audios/my_audios.html', context)


@login_required
@require_POST
def toggle_favorite(request, slug):
    """Toggle de favorito para un audio"""
    audio = get_object_or_404(Audio, slug=slug, status=Audio.Status.PUBLISHED)
    
    favorite, created = AudioFavorite.objects.get_or_create(
        user=request.user,
        audio=audio
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
        action = 'removed'
    else:
        is_favorite = True
        action = 'added'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite,
            'action': action,
            'favorites_count': audio.favorites_count
        })
    
    return redirect('audios:detail', slug=slug)


@login_required
def favorites_list(request):
    """Lista de audios favoritos del usuario"""
    favorites = AudioFavorite.objects.filter(user=request.user).select_related(
        'audio__seller', 'audio__category'
    ).order_by('-created_at')
    
    # Paginación
    paginator = Paginator(favorites, 12)
    page = request.GET.get('page')
    favorites_page = paginator.get_page(page)
    
    context = {
        'favorites': favorites_page
    }
    
    return render(request, 'audios/favorites.html', context)


@login_required
def add_review(request, slug):
    """Agregar reseña a un audio"""
    audio = get_object_or_404(Audio, slug=slug, status=Audio.Status.PUBLISHED)
    
    # No permitir reseñas propias
    if request.user == audio.seller:
        messages.error(request, 'No puedes reseñar tus propios audios.')
        return redirect('audios:detail', slug=slug)
    
    # Verificar si ya tiene una reseña
    existing_review = AudioReview.objects.filter(user=request.user, audio=audio).first()
    
    if request.method == 'POST':
        form = AudioReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.audio = audio
            review.save()
            
            action = 'actualizada' if existing_review else 'agregada'
            messages.success(request, f'Reseña {action} exitosamente.')
            return redirect('audios:detail', slug=slug)
    else:
        form = AudioReviewForm(instance=existing_review)
    
    context = {
        'form': form,
        'audio': audio,
        'existing_review': existing_review
    }
    
    return render(request, 'audios/add_review.html', context)


def category_detail(request, slug):
    """Audios de una categoría específica"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    audios = Audio.objects.filter(
        category=category,
        status=Audio.Status.PUBLISHED
    ).select_related('seller', 'genre').order_by('-published_at')
    
    # Paginación
    paginator = Paginator(audios, 12)
    page = request.GET.get('page')
    audios_page = paginator.get_page(page)
    
    # Géneros disponibles en esta categoría
    genres = Genre.objects.filter(
        category=category,
        is_active=True,
        audios__status=Audio.Status.PUBLISHED
    ).distinct().annotate(
        audio_count=Count('audios', filter=Q(audios__status=Audio.Status.PUBLISHED))
    )
    
    context = {
        'category': category,
        'audios': audios_page,
        'genres': genres,
        'total_audios': audios.count()
    }
    
    return render(request, 'audios/category_detail.html', context)


def seller_profile(request, username):
    """Perfil público de un vendedor"""
    seller = get_object_or_404(User, username=username, user_type='seller')
    
    audios = Audio.objects.filter(
        seller=seller,
        status=Audio.Status.PUBLISHED
    ).select_related('category', 'genre').order_by('-published_at')
    
    # Estadísticas del vendedor
    stats = {
        'total_audios': audios.count(),
        'total_downloads': sum(audio.downloads_count for audio in audios),
        'avg_rating': AudioReview.objects.filter(
            audio__seller=seller
        ).aggregate(avg=Avg('rating'))['avg'] or 0,
        'total_reviews': AudioReview.objects.filter(audio__seller=seller).count()
    }
    
    # Paginación
    paginator = Paginator(audios, 12)
    page = request.GET.get('page')
    audios_page = paginator.get_page(page)
    
    context = {
        'seller': seller,
        'audios': audios_page,
        'stats': stats
    }
    
    return render(request, 'audios/seller_profile.html', context)


@login_required
@require_POST
def delete_audio(request, slug):
    """Eliminar audio (solo el propietario)"""
    audio = get_object_or_404(Audio, slug=slug, seller=request.user)
    
    title = audio.title
    audio.delete()
    
    messages.success(request, f'Audio "{title}" eliminado exitosamente.')
    return redirect('audios:my_audios')


# API endpoints para AJAX
@login_required
def search_suggestions(request):
    """Sugerencias de búsqueda para autocomplete"""
    query = request.GET.get('q', '')
    suggestions = []
    
    if len(query) >= 2:
        # Buscar en títulos
        titles = Audio.objects.filter(
            title__icontains=query,
            status=Audio.Status.PUBLISHED
        ).values_list('title', flat=True)[:5]
        
        # Buscar en nombres de vendedores
        sellers = User.objects.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query),
            user_type='seller'
        ).values_list('first_name', 'last_name')[:3]
        
        suggestions.extend(list(titles))
        suggestions.extend([f"{first} {last}".strip() for first, last in sellers])
    
    return JsonResponse({'suggestions': suggestions[:8]})


@login_required
def change_audio_status(request, slug):
    """Cambiar el estado de un audio"""
    # Solo aceptar POST
    if request.method != 'POST':
        messages.error(request, 'Método no permitido.')
        return redirect('audios:my_audios')
    
    audio = get_object_or_404(Audio, slug=slug, seller=request.user)
    new_status = request.POST.get('status')
    
    # Debug: imprimir datos recibidos
    print(f"DEBUG: Cambiando estado de '{audio.title}' de '{audio.status}' a '{new_status}'")
    
    # Validar que el nuevo estado sea válido
    valid_statuses = [choice[0] for choice in Audio.Status.choices]
    if new_status not in valid_statuses:
        messages.error(request, f'Estado inválido: {new_status}. Estados válidos: {valid_statuses}')
        return redirect('audios:my_audios')
    
    old_status = audio.status
    audio.status = new_status
    
    # Si se está publicando, establecer fecha de publicación
    if new_status == Audio.Status.PUBLISHED and old_status != Audio.Status.PUBLISHED:
        from django.utils import timezone
        audio.published_at = timezone.now()
        print(f"DEBUG: Establecida fecha de publicación: {audio.published_at}")
    
    audio.save()
    print(f"DEBUG: Audio guardado con estado: {audio.status}")
    
    # Mensajes informativos
    status_messages = {
        Audio.Status.DRAFT: 'Audio guardado como borrador.',
        Audio.Status.PENDING: 'Audio enviado para revisión.',
        Audio.Status.PUBLISHED: 'Audio publicado exitosamente.',
        Audio.Status.INACTIVE: 'Audio marcado como inactivo.'
    }
    
    if new_status in status_messages:
        messages.success(request, status_messages[new_status])
    
    return redirect('audios:my_audios')
