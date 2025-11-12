from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import transaction  # Para asegurar la creación de ambos
from .forms import UserForm, PersonaForm
from django.contrib.auth.decorators import login_required  # <-- 1. Importamos el decorador


# Vista de Home (solo renderiza el template)
def home_view(request):
    return render(request, 'home.html')


# --- 2. AÑADIMOS LA NUEVA VISTA DE PERFIL ---
@login_required  # Esto protege la vista, solo usuarios logueados pueden entrar
def profile_view(request):
    """
    Muestra la página de perfil del usuario logueado.
    """
    # Gracias a la relación 1 a 1 y el 'related_name',
    # podemos acceder al perfil de la persona directamente desde el usuario.
    try:
        # Buscamos la persona asociada a este usuario
        persona = request.user.persona
    except Exception:
        # Caso borde: un superusuario creado por consola podría no tener
        # un objeto Persona asociado.
        persona = None

    context = {
        'persona': persona
    }
    # Renderizamos un NUEVO template que crearemos a continuación
    return render(request, 'personas/profile.html', context)


# Vista de Registro (Sign Up)
@transaction.atomic  # Decorador para hacer la operación "atómica"
def signup_view(request):
    if request.method == 'POST':
        # Si el método es POST, procesamos los datos del formulario
        user_form = UserForm(request.POST)
        persona_form = PersonaForm(request.POST)

        # Validamos ambos formularios
        if user_form.is_valid() and persona_form.is_valid():
            # 1. Guardamos el User (pero no en la BD aún, solo en memoria)
            user = user_form.save(commit=False)

            # 2. Encriptamos la contraseña
            user.set_password(user_form.cleaned_data['password'])

            # 3. Guardamos el User en la BD
            user.save()

            # 4. Guardamos la Persona (pero no en la BD aún)
            persona = persona_form.save(commit=False)

            # 5. Vinculamos la Persona con el User recién creado
            persona.user = user

            # 6. Guardamos la Persona en la BD
            persona.save()

            # 7. Hacemos login automáticamente al nuevo usuario
            login(request, user)

            # 8. Redirigimos al Home
            return redirect('home')
    else:
        # Si el método es GET, mostramos los formularios vacíos
        user_form = UserForm()
        persona_form = PersonaForm()

    # Preparamos el contexto para el template
    context = {
        'user_form': user_form,
        'persona_form': persona_form
    }
    # Renderizamos el template de registro
    return render(request, 'registration/signup.html', context)