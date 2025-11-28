from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Persona(models.Model):
    # --- 1. DEFINIR LAS OPCIONES DE ROL AQUÍ ---
    class Rol(models.TextChoices):
        CLIENTE = 'CLIENTE', _('Cliente')
        EMPRESARIO = 'EMPRESARIO', _('Empresario')
        ADMINISTRADOR = 'ADMIN', _('Administrador')

    class Genero(models.TextChoices):
        MASCULINO = 'M', _('Masculino')
        FEMENINO = 'F', _('Femenino')
        OTRO = 'O', _('Otro')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona')
    foto = models.ImageField(upload_to='personas/fotos/', null=True, blank=True)

    # --- 2. AGREGAR EL CAMPO ROL ---
    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.CLIENTE,
        verbose_name=_('Rol')
    )

    nombre = models.CharField(max_length=30, null=True, blank=True)
    apellido = models.CharField(max_length=30, null=True, blank=True)
    genero = models.CharField(max_length=1, choices=Genero.choices, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    estado = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"