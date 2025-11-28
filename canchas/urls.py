from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# Importamos settings y static para las imágenes
from django.conf import settings
from django.conf.urls.static import static

# Importamos TU vista personalizada
from apps.personas.views import home_view, profile_view, profile_edit_view, login_register_view, mis_reservas_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- CAMBIO IMPORTANTE AQUÍ ---
    # Usamos login_register_view en lugar de LoginView.as_view(...)
    # Esto carga tu lógica de login Y registro combinados.
    path('', login_register_view, name='login'),

    # Esta ruta la mantenemos por si acaso (para redirecciones internas),
    # apuntando a la misma vista.
    path('login_register/', login_register_view, name='login_register'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Rutas de App
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('home/', home_view, name='home'),
    path('empresas/', include('apps.empresas.urls')),
    path('mis-reservas/', mis_reservas_view, name='mis_reservas'),
]

# Configuración para servir imágenes en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
