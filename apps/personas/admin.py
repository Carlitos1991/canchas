from django.contrib import admin
from .models import Persona


# Register your models here.

@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    """
    Configuración personalizada para el modelo Persona en el admin.
    """
    # Muestra estos campos en la lista
    list_display = ('user', 'nombre', 'apellido', 'celular', 'estado')

    # Permite buscar por estos campos
    search_fields = ('nombre', 'apellido', 'user__username')

    # Añade filtros en la barra lateral
    list_filter = ('estado', 'genero')

    # Muestra los campos de auditoría como solo lectura
    readonly_fields = ('creado_en', 'actualizado_en')