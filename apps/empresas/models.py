from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Empresa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empresas')
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Empresa")
    gerente = models.CharField(max_length=100, verbose_name="Gerente General")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    ubicacion_url = models.URLField(verbose_name="Enlace Google Maps", blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono de Contacto")
    estado = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.nombre

class Cancha(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='canchas')
    nombre = models.CharField(max_length=50, verbose_name="Nombre de la Cancha")
    capacidad = models.PositiveIntegerField(verbose_name="Capacidad (Jugadores)", help_text="Ej: 10 para 5v5")
    precio_hora = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio por Hora")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"

    @property
    def foto_principal(self):
        return self.fotos.first()

class FotoCancha(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='fotos')
    imagen = models.ImageField(upload_to='canchas/fotos/')

# --- NUEVO MODELO DE DISPONIBILIDAD ---

class Disponibilidad(models.Model):
    """
    Representa un bloque de tiempo disponible para una cancha específica.
    """
    class Estado(models.TextChoices):
        LIBRE = 'LIBRE', _('Libre')
        PENDIENTE = 'PENDIENTE', _('Pendiente de Confirmación')
        RESERVADO = 'RESERVADO', _('Reservado')

    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE, related_name='disponibilidades')
    fecha = models.DateField(verbose_name=_("Fecha"))
    hora_inicio = models.TimeField(verbose_name=_("Hora de Inicio"))
    hora_fin = models.TimeField(verbose_name=_("Hora de Fin"))
    
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.LIBRE,
        verbose_name=_("Estado")
    )
    
    # Relación con el cliente que reserva. Es opcional (null=True).
    # Usamos settings.AUTH_USER_MODEL para una mejor práctica.
    # on_delete=models.SET_NULL para que si se borra el usuario, la reserva no se borre (se puede reasignar o cancelar).
    cliente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas',
        verbose_name=_("Cliente")
    )

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Disponibilidad de Cancha")
        verbose_name_plural = _("Disponibilidades de Canchas")
        # Evita que se pueda crear el mismo horario para la misma cancha dos veces.
        unique_together = ('cancha', 'fecha', 'hora_inicio')
        ordering = ['fecha', 'hora_inicio']

    def __str__(self):
        return f"{self.cancha.nombre} - {self.fecha} de {self.hora_inicio} a {self.hora_fin} ({self.get_estado_display()})"