from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

# --- Importamos nuestras vistas ---
from apps.personas.views import home_view, profile_view, profile_edit_view, login_register_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- RUTAS DE AUTENTICACIÓN ---

    # La raíz (/) es la página combinada de Login y Registro
    path('', login_register_view, name='login_register'),

    # El Logout redirige a la nueva de login (configurado en settings.py)
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- RUTAS DE LA APLICACIÓN ---

    # El "Home" (después de iniciar sesión)
    path('home/', home_view, name='home'),

    # Perfil y Edición de Perfil
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
]

# --- SERVIR ARCHIVOS MULTIMEDIA EN DESARROLLO ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)