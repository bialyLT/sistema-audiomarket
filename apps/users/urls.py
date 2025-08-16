from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    # Autenticación
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.custom_login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='core:home'), name='logout'),
    
    # Perfil
    path('profile/', views.profile_view, name='profile'),
    
    # Dashboards por tipo de usuario
    path('dashboard/buyer/', views.dashboard_buyer, name='dashboard_buyer'),
    path('dashboard/seller/', views.dashboard_seller, name='dashboard_seller'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
]
