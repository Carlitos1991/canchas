from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
# Importamos settings y static para las imágenes
from django.conf import settings
from django.conf.urls.static import static

from apps.empresas.views import api_listar_canchas, obtener_horarios_cancha
from apps.personas.views import api_login_movil
# Importamos TU vista personalizada
from apps.personas.views import home_view, profile_view, profile_edit_view, login_register_view, mis_reservas_view, \
    cancelar_reserva, admin_usuarios_view, update_user_role, get_user_profile_api, crear_usuario_view, \
    toggle_vista_cliente

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
    path('api/login/', api_login_movil, name='api_login_movil'),
    path('api/canchas/', api_listar_canchas, name='api_listar_canchas'),
    path('api/canchas/<int:cancha_id>/horarios/', obtener_horarios_cancha, name='api_horarios'),
    # Rutas de App
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('home/', home_view, name='home'),
    path('empresas/', include('apps.empresas.urls')),
    path('mis-reservas/', mis_reservas_view, name='mis_reservas'),
    path('api/cancelar-reserva/', cancelar_reserva, name='api_cancelar_reserva'),
    # GESTIÓN DE USUARIOS (Custom Admin)
    path('admin-usuarios/', admin_usuarios_view, name='admin_usuarios'),
    path('api/update-user/', update_user_role, name='update_user_role'),
    path('api/get-user-profile/<int:user_id>/', get_user_profile_api, name='get_user_profile_api'),
    path('crear-usuario/', crear_usuario_view, name='crear_usuario'),
    path('toggle-vista-cliente/', toggle_vista_cliente, name='toggle_vista_cliente'),
]

# Configuración para servir imágenes en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
