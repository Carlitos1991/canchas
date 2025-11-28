from django.urls import path
from . import views

urlpatterns = [
    path('gestion/', views.gestion_canchas_view, name='gestion_canchas'),

    # --- API Endpoints para AJAX ---
    path('api/empresa/save/', views.guardar_empresa, name='save_empresa'),
    path('api/cancha/save/', views.guardar_cancha, name='save_cancha'),
    path('api/disponibilidad/save/', views.guardar_disponibilidad, name='save_disponibilidad'),

    # --- Vistas de Fallback ---
    path('nueva/', views.nueva_cancha_view, name='nueva_cancha'),
    path('api/reservar/', views.reservar_horario, name='api_reservar'),
]
