from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Empresa, Cancha, FotoCancha, Disponibilidad
from . import forms as forms_module
from django.db import transaction
import json


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
    return render(request, 'apps/empresas/templates/gestion.html', context)


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
