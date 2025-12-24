from django.urls import path
from . import views
from .views import api_listar_canchas

urlpatterns = [
    path('gestion/', views.gestion_canchas_view, name='gestion_canchas'),

    # --- Vistas de Cliente ---
    path('empresa/<int:empresa_id>/canchas/', views.ver_canchas_empresa, name='ver_canchas_empresa'),
    path('cancha/<int:cancha_id>/horarios/', views.obtener_horarios_cancha, name='obtener_horarios_cancha'),

    # --- API Endpoints para AJAX ---
    path('api/empresa/save/', views.guardar_empresa, name='save_empresa'),
    path('api/cancha/save/', views.guardar_cancha, name='save_cancha'),
    path('api/disponibilidad/save/', views.guardar_disponibilidad, name='save_disponibilidad'),
    path('api/reservar/', views.reservar_horario, name='api_reservar'),

    # --- Vistas de Fallback ---
    path('nueva/', views.nueva_cancha_view, name='nueva_cancha'),
    path('save-empresa/', views.guardar_empresa, name='guardar_empresa'),
    path('api/canchas/', api_listar_canchas, name='api_listar_canchas'),
]
