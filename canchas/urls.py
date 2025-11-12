from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views  # Vistas de auth de Django

# --- 1. Importamos TODAS las vistas que necesitamos ---
from apps.personas.views import home_view, signup_view, profile_view, profile_edit_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- URLs de Autenticación ---

    # Esta es la ruta raíz (''). Es el LOGIN
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True  # Redirige si ya está logueado
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- URLs de la App Personas ---
    path('signup/', signup_view, name='signup'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),

    # Esta es la ruta 'home/' (a donde vamos DESPUÉS del login)
    path('home/', home_view, name='home'),
]