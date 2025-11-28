from django.urls import reverse


def sidebar_menu(request):
    """
    Inyecta la variable 'sidebar_menu' en todos los templates.
    Define los ítems del menú dinámicamente según el rol.
    """

    if not request.user.is_authenticated:
        return {}

    menu_items = []

    # Verificar si el admin está en "modo vista de cliente"
    vista_cliente_activa = request.session.get('vista_cliente', False)

    # --- 1. MENÚ PRINCIPAL (SEGÚN ROL) ---

    # Si es Empresario O Superusuario -> Ve el menú de Gestión
    if (request.user.groups.filter(name='Empresarios').exists() or request.user.is_superuser) and not vista_cliente_activa:
        menu_items.extend([
            {
                'label': 'Dashboard',
                'url': reverse('home'),
                'icon': 'fa-chart-line',
                'active_check': 'home'
            },
            {
                'label': 'Mis Empresas',
                'url': reverse('gestion_canchas'),
                'icon': 'fa-building',
                'active_check': 'gestion_canchas'
            },
        ])

    # Si es Cliente O el admin activó vista de cliente
    else:
        menu_items.extend([
            {
                'label': 'Buscar Canchas',
                'url': reverse('home'),
                'icon': 'fa-magnifying-glass',
                'active_check': 'home'
            },
            {
                'label': 'Mis Reservas',
                'url': reverse('mis_reservas'),
                'icon': 'fa-calendar-check',
                'active_check': 'mis_reservas'
            },
        ])

    # --- 2. MENÚ EXTRA PARA ADMINISTRADORES ---

    if request.user.is_superuser and not vista_cliente_activa:
        menu_items.insert(1, {  # Lo insertamos en segunda posición (debajo de Dashboard)
            'label': 'Usuarios',
            'url': reverse('admin_usuarios'),
            'icon': 'fa-users-gear',
            'active_check': 'admin_usuarios'
        })
        
        # Agregar opción para cambiar a vista de cliente
        menu_items.append({
            'label': 'Vista de Cliente',
            'url': reverse('toggle_vista_cliente'),
            'icon': 'fa-eye',
            'active_check': 'vista_cliente',
            'class': 'menu-toggle-vista'
        })

    # Si está en vista de cliente, agregar opción para volver
    if request.user.is_superuser and vista_cliente_activa:
        menu_items.append({
            'label': 'Volver a Admin',
            'url': reverse('toggle_vista_cliente'),
            'icon': 'fa-user-shield',
            'active_check': '',
            'class': 'menu-toggle-vista-admin'
        })

    # --- 3. RETORNO FINAL ---
    return {
        'sidebar_menu': menu_items,
        'vista_cliente_activa': vista_cliente_activa
    }
