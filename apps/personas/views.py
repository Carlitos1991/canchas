from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserForm, PersonaForm, UserEditForm
from .models import Persona


@login_required
def home_view(request):
    """
    Vista para la página de inicio (después del login).
    """
    return render(request, "home.html")


def signup_view(request):
    """
    Vista para el registro de nuevos usuarios (simplificado).
    """
    if request.method == 'POST':
        # --- NUEVA LÓGICA DE REGISTRO ---
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            # 1. Guardamos el User (con la contraseña hasheada)
            new_user = user_form.save()
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            # 2. ¡Importante! Creamos la Persona vacía asociada al usuario
            Persona.objects.create(user=new_user)

            # 3. Logueamos al usuario automáticamente
            login(request, new_user)

            # 4. Mensaje de bienvenida
            messages.success(request, '¡Bienvenido! Tu cuenta ha sido creada. Por favor, completa tu perfil.')

            # 5. Redirigimos a la página de "Editar Perfil"
            return redirect('profile_edit')
        # Si el formulario no es válido, se renderizará de nuevo
        # con los errores (el 'else' de abajo se encarga).

    else:  # Si es un GET
        user_form = UserForm()

    # Preparamos el contexto (solo con user_form)
    context = {
        'user_form': user_form
    }
    return render(request, 'registration/signup.html', context)
    # --- FIN DE LA NUEVA LÓGICA ---


@login_required
def profile_view(request):
    """
    Vista para mostrar el perfil del usuario.
    """
    # Usamos get_object_or_404 para manejar el caso de que la persona no exista
    # (aunque ahora siempre debería existir)
    persona = get_object_or_404(Persona, user=request.user)
    context = {
        'persona': persona
    }
    return render(request, 'personas/profile.html', context)


@login_required
def profile_edit_view(request):
    """
    Vista para editar el perfil del usuario.
    """
    persona = get_object_or_404(Persona, user=request.user)

    if request.method == 'POST':
        # Pasamos 'instance' para que los formularios sepan qué objetos editar
        user_form = UserEditForm(request.POST, instance=request.user)
        persona_form = PersonaForm(request.POST, instance=persona)

        if user_form.is_valid() and persona_form.is_valid():
            user_form.save()
            persona_form.save()

            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')

            # Redirigimos al perfil para ver los cambios
            return redirect('profile')

    else:  # Si es un GET
        # Llenamos los formularios con la data actual
        user_form = UserEditForm(instance=request.user)
        persona_form = PersonaForm(instance=persona)

    context = {
        'user_form': user_form,
        'persona_form': persona_form
    }
    return render(request, 'personas/profile_edit.html', context)