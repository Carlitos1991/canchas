# apps/personas/context_processors.py
from django.urls import reverse


def sidebar_menu(request):
    """
    Inyecta la variable 'sidebar_menu' en todos los templates.
    Define los ítems del menú dinámicamente según el rol.
    """
    if not request.user.is_authenticated:
        return {}

    menu_items = []

    # --- MENÚ COMÚN (Perfil) ---
    # (Opcional, si quieres que aparezca en la lista principal aparte del dropdown)

    # --- MENÚ DE EMPRESARIOS ---
    if request.user.groups.filter(name='Empresarios').exists() or request.user.is_superuser:
        menu_items.extend([
            {
                'label': 'Dashboard',
                'url': reverse('home'),
                'icon': 'fa-chart-line',
                'active_check': 'home'
            },
            {
                'label': 'Mis Empresas',
                # Si usas namespace: reverse('empresas:gestion_canchas')
                # Si NO usas namespace (como lo tienes ahora):
                'url': reverse('gestion_canchas'),
                'icon': 'fa-briefcase',
                'active_check': 'gestion_canchas'
            },
        ])

    # --- MENÚ DE CLIENTES ---
    else:
        menu_items.extend([
            {
                'label': 'Buscar Canchas',
                'url': reverse('home'),
                'icon': 'fa-futbol',
                'active_check': 'home'
            },
            {
                'label': 'Mis Reservas',
                'url': reverse('mis_reservas'),  # Necesitaremos crear esta vista
                'icon': 'fa-calendar-check',
                'active_check': 'mis_reservas'
            },
        ])

    return {'sidebar_menu': menu_items}
