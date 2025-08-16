from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class AdminAccessMiddleware:
    """
    Middleware que restringe el acceso al admin de Django solo a usuarios admin
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verificar si la ruta es del admin
        if request.path.startswith('/admin/'):
            # Permitir acceso a la página de login del admin
            if request.path == '/admin/login/' or request.path == '/admin/logout/':
                response = self.get_response(request)
                return response
            
            # Verificar que el usuario esté autenticado y sea admin
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder al panel de administración.')
                return redirect('users:login')
            
            # Verificar que el usuario sea admin o staff
            if not (request.user.is_admin_user or request.user.is_staff or request.user.is_superuser):
                messages.error(request, 'No tienes permisos para acceder al panel de administración.')
                return redirect('core:home')

        response = self.get_response(request)
        return response
