from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm, PersonaForm, UserEditForm
from .models import Persona


# --- ¡NUEVA VISTA COMBINADA! ---
def login_register_view(request):
    """
    Maneja tanto el inicio de sesión como el registro en una sola página.
    """

    # --- Lógica de Registro (Sign Up) ---
    # Si los datos vienen del formulario de registro...
    if request.method == 'POST' and 'signup_submit' in request.POST:
        user_form = UserForm(request.POST, prefix='signup')

        if user_form.is_valid():
            user = user_form.save()
            # Creamos una Persona vacía
            Persona.objects.create(user=user)
            # Logueamos al usuario
            login(request, user)
            # Redirigimos a "Editar Perfil" para que complete sus datos
            return redirect('profile_edit')
        else:
            # Si el formulario de registro no es válido, mostramos los errores
            # Creamos un formulario de login vacío para mostrar en la otra pestaña
            login_form = AuthenticationForm(prefix='login')
            # Le decimos al template que muestre el panel de registro activo
            return render(request, 'registration/login_register.html', {
                'user_form': user_form,
                'login_form': login_form,
                'show_signup': True  # Variable para activar el panel de JS
            })

    # --- Lógica de Inicio de Sesión (Login) ---
    # Si los datos vienen del formulario de login...
    elif request.method == 'POST' and 'login_submit' in request.POST:
        # Reutilizamos UserForm para el login, pero solo usamos username/password
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Este formulario maneja la autenticación y los errores de "clave incorrecta"
        login_form = AuthenticationForm(request, data=request.POST, prefix='login')
        if login_form.is_valid():
            # --- CAMBIO AQUÍ: Usamos el form para loguear ---
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:
            # El form ya tiene los errores (ej. "usuario o clave incorrecta")
            # --- CAMBIO AQUÍ: Creamos un form de registro vacío ---
            user_form = UserForm(prefix='signup')
            return render(request, 'registration/login_register.html', {
                'user_form': user_form,
                'login_form': login_form,
                'show_signup': False
            })

    # --- Lógica GET (Carga inicial de la página) ---
    else:
        # Si es un GET, mostramos ambos formularios vacíos
        user_form = UserForm(prefix='signup')
        login_form = AuthenticationForm(prefix='login')  # Usamos UserForm también para login por simplicidad de campos

    return render(request, 'registration/login_register.html', {
        'user_form': user_form,
        'login_form': login_form
    })


# --- VISTAS PROTEGIDAS (Sin cambios) ---

@login_required
def home_view(request):
    """
    Vista para la página de inicio, visible solo para usuarios logueados.
    """
    return render(request, 'home.html')


@login_required
def profile_view(request):
    """
    Muestra el perfil del usuario logueado.
    """
    # CORRECCIÓN: Obtener el objeto 'persona' y pasarlo al contexto.
    # Usamos getattr para evitar un error si la persona no existe por alguna razón.
    persona = getattr(request.user, 'persona', None)
    
    # Pasamos la variable 'persona' a la plantilla.
    return render(request, 'personas/profile.html', {'persona': persona})


@login_required
def profile_edit_view(request):
    """
    Permite al usuario logueado editar su User (email) y su Persona.
    """
    user = request.user
    # Usamos 'getattr' para manejar el caso de que 'persona' no exista
    persona = getattr(user, 'persona', None)

    # Si no tiene persona (creado por admin), la creamos
    if not persona:
        persona = Persona.objects.create(user=user)

    if request.method == 'POST':
        # Pasamos la instancia existente para que el formulario sepa que es una edición
        user_form = UserEditForm(request.POST, instance=user)
        # CORRECCIÓN: Añadimos request.FILES para manejar la subida de la foto
        persona_form = PersonaForm(request.POST, request.FILES, instance=persona)

        if user_form.is_valid() and persona_form.is_valid():
            user_form.save()
            persona_form.save()
            return redirect('profile')  # Redirigir al perfil para ver los cambios
    else:
        # Creamos los formularios precargados con la info actual
        user_form = UserEditForm(instance=user)
        persona_form = PersonaForm(instance=persona)

    return render(request, 'personas/profile_edit.html', {
        'user_form': user_form,
        'persona_form': persona_form
    })