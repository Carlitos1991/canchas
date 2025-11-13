from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

# --- Importamos nuestras vistas ---
from apps.personas.views import home_view, profile_view, profile_edit_view, login_register_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- RUTAS DE AUTENTICACIÓN (ACTUALIZADAS) ---

    # La raíz (/) ahora es nuestra página combinada de Login y Registro
    path('', login_register_view, name='login_register'),

    # El Logout nos redirige a la nueva página de login (configurado en settings.py)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- RUTAS DE LA APLICACIÓN ---

    # El "Home" (después de iniciar sesión)
    path('home/', home_view, name='home'),

    # Perfil y Edición de Perfil
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
]