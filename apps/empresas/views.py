from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Empresa, Cancha, FotoCancha, Disponibilidad
from . import forms as forms_module
from django.db import transaction
from datetime import datetime, date
import json


def api_listar_canchas(request):
    try:
        # Traemos todas las canchas activas
        canchas = Cancha.objects.filter(estado=True)

        lista_data = []
        for c in canchas:
            # --- CORRECCIÓN IMAGEN ---
            # Como las fotos están en otro modelo (FotoCancha), buscamos la primera asociada.
            # 'fotos' es el related_name que vi que usas en guardar_cancha
            primera_foto = c.fotos.first()

            imagen_url = None
            if primera_foto:
                imagen_url = primera_foto.imagen.url

            lista_data.append({
                'id': c.id,
                'nombre': c.nombre,
                'direccion': c.direccion if hasattr(c, 'direccion') else 'Dirección no disponible',
                'precio': str(c.precio_hora) if hasattr(c, 'precio_hora') else '0.00',
                'imagen': imagen_url  # Aquí pasamos la url real o None
            })

        return JsonResponse({'status': 'ok', 'canchas': lista_data})
    except Exception as e:
        print(f"ERROR API: {e}")  # Esto mostrará el error en la consola negra si vuelve a fallar
        return JsonResponse({'status': 'error', 'mensaje': str(e)}, status=500)


@login_required
def reservar_horario(request):
    """
    API AJAX para que un cliente reserve un horario.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            disponibilidad_id = data.get('disponibilidad_id')

            with transaction.atomic():
                # select_for_update bloquea la fila para evitar doble reserva concurrente
                slot = get_object_or_404(Disponibilidad.objects.select_for_update(), id=disponibilidad_id)

                if slot.estado != Disponibilidad.Estado.LIBRE:
                    return JsonResponse({'success': False, 'message': 'Este horario ya no está disponible.'})

                slot.estado = Disponibilidad.Estado.RESERVADO
                slot.cliente = request.user
                slot.save()

            return JsonResponse({'success': True, 'message': '¡Reserva confirmada exitosamente!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Método no permitido'})


def es_gestor(user):
    return user.is_superuser or user.groups.filter(name='Empresarios').exists()


@login_required
@user_passes_test(es_gestor)
def gestion_canchas_view(request):
    if request.user.is_superuser:
        empresas_qs = Empresa.objects.all()
    else:
        empresas_qs = request.user.empresas.all()

    # Optimizamos la consulta para traer las canchas y sus disponibilidades de una vez
    empresas = empresas_qs.prefetch_related('canchas__disponibilidades')

    empresa_id_param = request.GET.get('empresa_id')
    active_empresa = None
    if empresa_id_param:
        query = {'id': empresa_id_param}
        if not request.user.is_superuser:
            query['user'] = request.user
        active_empresa = get_object_or_404(empresas_qs, **query)
    elif empresas.exists():
        active_empresa = empresas.first()

    # Las canchas ya vienen precargadas en el objeto active_empresa
    canchas = active_empresa.canchas.all() if active_empresa else []

    context = {
        'empresas': empresas,
        'active_empresa': active_empresa,
        'canchas': canchas,
        'empresa_form': forms_module.EmpresaForm(instance=active_empresa),
        'cancha_form': forms_module.CanchaForm(),
        'disponibilidad_form': forms_module.DisponibilidadForm(),  # <-- Nuevo formulario
    }
    return render(request, 'empresas/gestion.html', context)


@login_required
@user_passes_test(es_gestor)
def guardar_empresa(request):
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa_id')
        instance = None
        if empresa_id:
            query = {'id': empresa_id}
            if not request.user.is_superuser:
                query['user'] = request.user
            instance = get_object_or_404(Empresa, **query)
        form = forms_module.EmpresaForm(request.POST, instance=instance)
        if form.is_valid():
            empresa = form.save(commit=False)
            if not instance:
                empresa.user = request.user
            empresa.save()
            return JsonResponse({'success': True, 'message': 'Información de empresa guardada.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
@user_passes_test(es_gestor)
def guardar_cancha(request):
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa_id')
        if not empresa_id:
            return JsonResponse({'success': False, 'message': 'Se requiere una empresa.'})
        query = {'id': empresa_id}
        if not request.user.is_superuser:
            query['user'] = request.user
        empresa = get_object_or_404(Empresa, **query)
        cancha_id = request.POST.get('cancha_id')
        instance = get_object_or_404(Cancha, id=cancha_id, empresa=empresa) if cancha_id else None
        form = forms_module.CanchaForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            cancha = form.save(commit=False)
            cancha.empresa = empresa
            cancha.save()
            if instance and request.FILES.getlist('fotos'):
                instance.fotos.all().delete()
            for f in request.FILES.getlist('fotos'):
                FotoCancha.objects.create(cancha=cancha, imagen=f)
            return JsonResponse({'success': True, 'message': 'Cancha guardada.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
@user_passes_test(es_gestor)
def guardar_disponibilidad(request):
    """
    AJAX: Crea un nuevo horario de disponibilidad para una cancha.
    """
    if request.method == 'POST':
        cancha_id = request.POST.get('cancha_id')
        if not cancha_id:
            return JsonResponse({'success': False, 'message': 'Se requiere una cancha.'})

        # Verificar que el usuario tiene permiso sobre la cancha
        query = {'id': cancha_id}
        if not request.user.is_superuser:
            query['empresa__user'] = request.user
        cancha = get_object_or_404(Cancha, **query)

        form = forms_module.DisponibilidadForm(request.POST)
        if form.is_valid():
            disponibilidad = form.save(commit=False)
            disponibilidad.cancha = cancha
            disponibilidad.save()
            return JsonResponse({'success': True, 'message': 'Horario guardado.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


# --- Vistas de Fallback (si se mantienen) ---
@login_required
@user_passes_test(es_gestor)
def nueva_cancha_view(request):
    # ... (código existente, se puede revisar o eliminar si ya no se usa)
    pass


def ver_canchas_empresa(request, empresa_id):
    """
    Vista para mostrar todas las canchas de una empresa específica.
    Incluye filtrado por fecha y hora.
    """
    empresa = get_object_or_404(Empresa, id=empresa_id, estado=True)

    # Obtener parámetros de filtro
    fecha_filtro = request.GET.get('fecha')
    hora_filtro = request.GET.get('hora')

    # Consulta base de canchas
    canchas = Cancha.objects.filter(
        empresa=empresa,
        estado=True
    ).prefetch_related('fotos', 'disponibilidades')

    # Agregar disponibilidades libres a cada cancha
    for cancha in canchas:
        disponibilidades = cancha.disponibilidades.filter(estado='LIBRE')

        # Aplicar filtros si existen
        if fecha_filtro:
            disponibilidades = disponibilidades.filter(fecha=fecha_filtro)
        if hora_filtro:
            disponibilidades = disponibilidades.filter(hora_inicio=hora_filtro)

        # Ordenar por fecha y hora
        cancha.disponibilidades_libres = disponibilidades.order_by('fecha', 'hora_inicio')

    # Generar lista de horas disponibles para el select
    horas_disponibles = [
        '06:00', '07:00', '08:00', '09:00', '10:00', '11:00',
        '12:00', '13:00', '14:00', '15:00', '16:00', '17:00',
        '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'
    ]

    context = {
        'empresa': empresa,
        'canchas': canchas,
        'horas_disponibles': horas_disponibles,
        'fecha_filtro': fecha_filtro,
        'today': date.today().isoformat(),
    }

    return render(request, 'empresas/ver_canchas_empresa.html', context)


def obtener_horarios_cancha(request, cancha_id):
    """
    API AJAX para obtener todos los horarios de una cancha.
    """
    cancha = get_object_or_404(Cancha, id=cancha_id, estado=True)

    # Obtener todas las disponibilidades futuras
    disponibilidades = cancha.disponibilidades.filter(
        fecha__gte=date.today()
    ).order_by('fecha', 'hora_inicio')

    horarios_data = []
    for d in disponibilidades:
        horarios_data.append({
            'id': d.id,
            'fecha': d.fecha.isoformat(),
            'hora_inicio': d.hora_inicio.strftime('%H:%M'),
            'hora_fin': d.hora_fin.strftime('%H:%M'),
            'estado': d.estado,
        })

    return JsonResponse({
        'success': True,
        'cancha': {
            'id': cancha.id,
            'nombre': cancha.nombre,
            'precio': float(cancha.precio_hora),
        },
        'horarios': horarios_data
    })
