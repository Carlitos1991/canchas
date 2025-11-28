from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserEditForm, UserLoginForm, PersonaForm
from .models import Persona
from apps.empresas.models import Cancha


# --- VISTA HOME (DISPATCHER) ---
@login_required
def home_view(request):
    user = request.user
    # 1. Si es Empresario/Admin -> Dashboard Gerente
    if user.is_superuser or user.groups.filter(name='Empresarios').exists():
        return render(request, 'empresas/dashboard_manager.html')
    # 2. Si es Cliente -> Dashboard Cliente
    canchas = Cancha.objects.filter(estado=True).select_related('empresa').prefetch_related('disponibilidades')
    return render(request, 'empresas/dashboard_cliente.html', {'canchas': canchas})


# --- VISTA LOGIN / REGISTRO ---
def login_register_view(request):
    """
    Maneja tanto el inicio de sesión como el registro en una sola página.
    """
    # 1. Lógica de Registro (Sign Up)
    if request.method == 'POST' and 'signup_submit' in request.POST:
        user_form = UserForm(request.POST, prefix='signup')

        if user_form.is_valid():
            user = user_form.save()
            # Asignamos ROL CLIENTE automáticamente
            Persona.objects.create(user=user, rol=Persona.Rol.CLIENTE)
            login(request, user)
            return redirect('profile_edit')
        else:
            # Si falla, mantenemos el panel de registro abierto
            login_form = UserLoginForm(prefix='login')
            return render(request, 'registration/login_register.html', {
                'user_form': user_form,
                'login_form': login_form,
                'show_signup': True
            })

    # 2. Lógica de Inicio de Sesión (Login)
    elif request.method == 'POST' and 'login_submit' in request.POST:
        login_form = UserLoginForm(request, data=request.POST, prefix='login')
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('home')
        else:
            user_form = UserForm(prefix='signup')
            return render(request, 'registration/login_register.html', {
                'user_form': user_form,
                'login_form': login_form,
                'show_signup': False
            })

    # 3. Carga inicial (GET)
    else:
        if request.user.is_authenticated:
            return redirect('home')
        user_form = UserForm(prefix='signup')
        login_form = UserLoginForm(prefix='login')

    return render(request, 'registration/login_register.html', {
        'user_form': user_form,
        'login_form': login_form
    })


# --- VISTAS DE PERFIL ---
@login_required
def profile_view(request):
    persona = getattr(request.user, 'persona', None)
    return render(request, 'personas/profile.html', {'persona': persona})


@login_required
def profile_edit_view(request):
    user = request.user
    persona = getattr(user, 'persona', None)
    if not persona:
        persona = Persona.objects.create(user=user, rol=Persona.Rol.CLIENTE)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        persona_form = PersonaForm(request.POST, request.FILES, instance=persona)
        if user_form.is_valid() and persona_form.is_valid():
            user_form.save()
            persona_form.save()
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=user)
        persona_form = PersonaForm(instance=persona)

    return render(request, 'personas/profile_edit.html', {
        'user_form': user_form,
        'persona_form': persona_form
    })

@login_required
def mis_reservas_view(request):
    """
    Vista para ver el historial de reservas del cliente.
    """
    # Por ahora renderizamos un template vacío
    return render(request, 'personas/mis_reservas.html')