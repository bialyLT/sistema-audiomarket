from django.urls import path
from . import views

app_name = 'audios'

urlpatterns = [
    # Listado y búsqueda
    path('', views.audio_list, name='list'),
    path('buscar/', views.audio_list, name='search'),
    
    # Gestión de audios del usuario (ANTES de slug para evitar conflictos)
    path('mis-audios/', views.my_audios, name='my_audios'),
    path('subir/', views.audio_upload, name='upload'),
    path('favoritos/', views.favorites_list, name='favorites'),
    
    # Categorías y vendedores
    path('categoria/<slug:slug>/', views.category_detail, name='category'),
    path('vendedor/<str:username>/', views.seller_profile, name='seller_profile'),
    
    # API endpoints
    path('api/buscar-sugerencias/', views.search_suggestions, name='search_suggestions'),
    
    # Detalle y acciones de audios (AL FINAL para evitar conflictos de slug)
    path('<slug:slug>/', views.audio_detail, name='detail'),
    path('<slug:slug>/favorito/', views.toggle_favorite, name='toggle_favorite'),
    path('<slug:slug>/reseña/', views.add_review, name='add_review'),
    path('<slug:slug>/editar/', views.audio_edit, name='edit'),
    path('<slug:slug>/eliminar/', views.delete_audio, name='delete'),
    path('<slug:slug>/cambiar-estado/', views.change_audio_status, name='change_status'),
]
