from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views, views  # Vistas de auth de Django

# --- 1. Importamos TODAS las vistas que necesitamos ---
from apps.personas.views import home_view, profile_view, profile_edit_view, mis_reservas_view, api_login_movil, \
    toggle_vista_cliente

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- URLs de Autenticación ---

    # --- AÑADIMOS UN PARÁMETRO AQUÍ ---
    path('', auth_views.LoginView.as_view(
        template_name='registration/login_register.html',
        redirect_authenticated_user=True  # <-- Esta es la línea mágica
    ), name='login'),
    # --- FIN DEL CAMBIO ---

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- 2. Movimos las URLs de 'personas' aquí ---
    # (Ya no usamos el include)
    # path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),

    # 3. Ruta de Home
    path('home/', home_view, name='home'),
    path('mis-reservas/', mis_reservas_view, name='mis_reservas'),
    path('api/login/', api_login_movil, name='api_login_movil'),
    path('toggle-vista/', toggle_vista_cliente, name='toggle_vista_cliente'),
    # --- 4. ELIMINAMOS EL INCLUDE PROBLEMÁTICO ---
    # path('', include('apps.personas.urls')),
]
