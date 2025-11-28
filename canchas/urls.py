from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.personas.views import home_view, profile_view, profile_edit_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Autenticación y Personas ---
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', profile_edit_view, name='profile_edit'),
    path('home/', home_view, name='home'),

    # --- AQUI ESTABA EL ERROR: FALTABA INCLUIR ESTA LÍNEA ---
    # Conectamos las URLs de la app 'empresas' para que 'gestion_canchas' exista.
    path('empresas/', include('apps.empresas.urls')),
]
