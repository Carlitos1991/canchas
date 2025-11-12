from django.urls import path
from .views import signup_view, profile_view  # <-- 1. Importamos la nueva vista

# Este archivo será incluido en el urls.py principal
urlpatterns = [
    # Ruta para la vista de registro
    path('signup/', signup_view, name='signup'),

    # --- 2. AÑADIMOS LA NUEVA RUTA DE PERFIL ---
    path('profile/', profile_view, name='profile'),
]