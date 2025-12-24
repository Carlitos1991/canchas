from django.shortcuts import render, redirect, get_object_or_404
import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from apps.empresas.models import Cancha, Disponibilidad  # Importamos Disponibilidad
from .forms import UserForm, UserEditForm, UserLoginForm, PersonaForm, PersonaAdminForm
from .models import Persona
from django.contrib.auth.models import User
from apps.empresas.models import Empresa


# --- VISTA HOME (DISPATCHER) ---
@login_required
@login_required
def home_view(request):
    user = request.user

    # 1. Verificamos si el usuario activó el "Modo Cliente" manualmente
    # (Esto busca una variable en la sesión del navegador)
    vista_cliente_activa = request.session.get('vista_cliente', False)

    # 2. Definimos si es Gestor (Admin o del grupo Empresarios)
    es_gestor = user.is_superuser or user.groups.filter(name='Empresarios').exists()

    # 3. LÓGICA DE DECISIÓN:
    # Si es gestor Y NO ha activado la vista de cliente -> Muestra Dashboard Manager
    if es_gestor and not vista_cliente_activa:
        return render(request, 'empresas/dashboard_manager.html')

    # 4. EN CUALQUIER OTRO CASO -> Muestra Dashboard Cliente (Lista de Empresas)
    else:
        # Traemos las empresas para listarlas
        empresas = Empresa.objects.filter(estado=True).prefetch_related('canchas')

        context = {
            'empresas': empresas,
            'vista_cliente_activa': vista_cliente_activa  # Para que base.html muestre el banner de aviso
        }
        return render(request, 'empresas/dashboard_cliente.html', context)


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
    # Usamos 'reservas' porque en el modelo Disponibilidad pusimos related_name='reservas'
    reservas = request.user.reservas.select_related('cancha', 'cancha__empresa').order_by('fecha', 'hora_inicio')

    return render(request, 'personas/mis_reservas.html', {
        'reservas': reservas
    })


@login_required
def cancelar_reserva(request):
    """
    API AJAX para cancelar una reserva propia.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            reserva_id = data.get('reserva_id')

            # Buscamos la reserva asegurándonos que pertenezca al usuario actual
            reserva = get_object_or_404(Disponibilidad, id=reserva_id, cliente=request.user)

            with transaction.atomic():
                reserva.cliente = None
                reserva.estado = Disponibilidad.Estado.LIBRE
                reserva.save()

            return JsonResponse({'success': True, 'message': 'Reserva cancelada exitosamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
@user_passes_test(lambda u: u.is_superuser)  # Solo superusuarios
def admin_usuarios_view(request):
    """
    Renderiza la tabla de todos los usuarios registrados.
    También procesa actualizaciones de usuarios desde el modal.
    """
    # Procesar formulario POST del modal
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        accion = request.POST.get('accion', 'editar')

        try:
            # Buscamos la Persona asociada al ID de usuario
            persona = get_object_or_404(Persona, user_id=user_id)

            if accion == 'cambiar_estado':
                # Solo cambiar el estado
                estado = request.POST.get('estado') == 'true'
                persona.estado = estado
                persona.save()

                from django.contrib import messages
                estado_texto = 'activado' if estado else 'dado de baja'
                messages.success(request, f'Usuario {persona.user.username} {estado_texto} correctamente.')
            else:
                # Edición completa: Actualizamos rol y estado
                rol = request.POST.get('rol')
                estado = request.POST.get('estado') == 'true'

                persona.rol = rol
                persona.estado = estado
                persona.save()

                # Mensaje de éxito
                from django.contrib import messages
                messages.success(request, f'Usuario {persona.user.username} actualizado correctamente.')

        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error al actualizar usuario: {str(e)}')

        # Redireccionar para evitar reenvío del formulario
        return redirect('admin_usuarios')

    # GET: Traemos Usuario y su perfil Persona para no hacer n+1 queries
    usuarios = User.objects.select_related('persona').all().order_by('-date_joined')

    # Calcular estadísticas
    activos_count = usuarios.filter(persona__estado=True).count()
    empresarios_count = usuarios.filter(persona__rol='EMPRESARIO').count()
    admins_count = usuarios.filter(persona__rol='ADMIN').count()

    context = {
        'usuarios': usuarios,
        'activos_count': activos_count,
        'empresarios_count': empresarios_count,
        'admins_count': admins_count,
        'form_admin': PersonaAdminForm()  # Formulario vacío para el Modal
    }
    return render(request, 'personas/admin_usuarios.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_user_role(request):
    """
    API AJAX para cambiar el rol o estado de un usuario.
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            # Buscamos la Persona asociada al ID de usuario
            persona = get_object_or_404(Persona, user_id=user_id)

            form = PersonaAdminForm(request.POST, instance=persona)
            if form.is_valid():
                form.save()
                # NOTA: Al hacer .save(), se dispara la SIGNAL que creamos antes
                # y actualiza los grupos automáticamente.
                return JsonResponse({'success': True, 'message': 'Usuario actualizado correctamente.'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_user_profile_api(request, user_id):
    """
    API para obtener el perfil completo de un usuario.
    """
    try:
        user = get_object_or_404(User, id=user_id)
        persona = user.persona

        data = {
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined.strftime('%d %b, %Y'),
            },
            'persona': {
                'nombre': persona.nombre or '',
                'apellido': persona.apellido or '',
                'celular': persona.celular or '',
                'fecha_nacimiento': persona.fecha_nacimiento.strftime('%d %b, %Y') if persona.fecha_nacimiento else '',
                'genero': persona.get_genero_display() if persona.genero else '',
                'direccion': persona.direccion or '',
                'rol': persona.rol,
                'estado': persona.estado,
                'foto': persona.foto.url if persona.foto else '',
                'actualizado_en': persona.actualizado_en.strftime('%d %b, %Y %H:%M'),
            }
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_usuario_view(request):
    """
    Vista para crear un nuevo usuario con su perfil de persona.
    Solo accesible por administradores.
    """
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            username = request.POST.get('username', '').strip()
            email = request.POST.get('email', '').strip()
            password = request.POST.get('password', '').strip()
            nombre = request.POST.get('nombre', '').strip()
            apellido = request.POST.get('apellido', '').strip()
            celular = request.POST.get('celular', '').strip()
            rol = request.POST.get('rol', 'CLIENTE')
            estado = request.POST.get('estado') == 'on'

            # Validaciones básicas
            if not username or not email or not password:
                from django.contrib import messages
                messages.error(request, 'Usuario, email y contraseña son obligatorios.')
                return redirect('admin_usuarios')

            if len(password) < 8:
                from django.contrib import messages
                messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
                return redirect('admin_usuarios')

            # Verificar si el username o email ya existen
            if User.objects.filter(username=username).exists():
                from django.contrib import messages
                messages.error(request, f'El nombre de usuario "{username}" ya está en uso.')
                return redirect('admin_usuarios')

            if User.objects.filter(email=email).exists():
                from django.contrib import messages
                messages.error(request, f'El email "{email}" ya está registrado.')
                return redirect('admin_usuarios')

            # Crear usuario y persona en una transacción atómica
            with transaction.atomic():
                # Crear el usuario
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                # Crear la persona asociada
                persona = Persona.objects.create(
                    user=user,
                    nombre=nombre,
                    apellido=apellido,
                    celular=celular,
                    rol=rol,
                    estado=estado
                )

                # La señal (signal) se encargará de asignar el grupo automáticamente
                # basándose en el rol de la persona

            from django.contrib import messages
            messages.success(request, f'Usuario "{username}" creado exitosamente con rol {persona.get_rol_display()}.')
            return redirect('admin_usuarios')

        except Exception as e:
            from django.contrib import messages
            messages.error(request, f'Error al crear usuario: {str(e)}')
            return redirect('admin_usuarios')

    # Si es GET, redirigir a admin usuarios
    return redirect('admin_usuarios')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def toggle_vista_cliente(request):
    """
    Permite a los administradores alternar entre su vista normal
    y la vista de cliente del sistema.
    """
    # Obtener estado actual
    vista_cliente_activa = request.session.get('vista_cliente', False)
    estado_actual = request.session.get('vista_cliente', False)
    request.session['vista_cliente'] = not estado_actual

    from django.contrib import messages
    if not vista_cliente_activa:
        messages.info(request, '👁️ Ahora estás viendo el sistema como un Cliente.')
    else:
        messages.info(request, '🛡️ Has vuelto a la vista de Administrador.')

    # Redirigir al home para que cargue la vista correspondiente
    return redirect('home')


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json


@csrf_exempt  # Desactiva la seguridad CSRF solo para esta vista (necesario para el celular)
def api_login_movil(request):
    if request.method == 'POST':
        try:
            # 1. Recibimos los datos del celular (JSON)
            data = json.loads(request.body)
            usuario_o_email = data.get('email')  # En el celular el campo se llama 'email'
            password = data.get('password')

            # 2. Lógica para permitir login con Email o Username
            user = authenticate(username=usuario_o_email, password=password)

            # Si falló, intentamos buscar si lo que ingresó fue un email
            if user is None:
                try:
                    user_obj = User.objects.get(email=usuario_o_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass

            # 3. Respondemos al celular
            if user is not None:
                if user.is_active:
                    # Buscamos los datos de la persona asociada
                    persona_nombre = "Usuario"
                    if hasattr(user, 'persona'):
                        persona_nombre = f"{user.persona.nombre} {user.persona.apellido}"

                    return JsonResponse({
                        'status': 'ok',
                        'mensaje': 'Login exitoso',
                        'user_id': user.id,
                        'nombre': persona_nombre,
                        'username': user.username
                    })
                else:
                    return JsonResponse({'status': 'error', 'mensaje': 'Usuario inactivo'}, status=401)
            else:
                return JsonResponse({'status': 'error', 'mensaje': 'Credenciales incorrectas'}, status=401)

        except Exception as e:
            return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'}, status=405)
