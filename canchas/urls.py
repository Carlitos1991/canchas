from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views # Vistas de auth de Django

# Importamos la vista home que crearemos
from apps.personas.views import home_view 

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- URLs de Autenticación ---

    # 1. Login y Logout (usando vistas incorporadas de Django)
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 2. Signup (y otras rutas de nuestra app 'personas')
    # Incluimos el archivo urls.py de nuestra app personas
    path('', include('apps.personas.urls')),

    # 3. Ruta de Home
    # La definimos aquí para que sea la raíz del sitio
    path('', home_view, name='home'),
]