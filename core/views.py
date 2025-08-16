from django.shortcuts import render


def home(request):
    """Vista principal del sitio."""
    context = {
        'title': 'Inicio - Proyecto de gestion',
        'welcome_message': 'Bienvenido al Sistema de Gestión',
    }
    return render(request, 'inicio/home.html', context)
