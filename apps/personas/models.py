from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Persona(models.Model):
    """
    Modelo que extiende el User de Django con una relación OneToOne.
    Contiene la información personal y demográfica del usuario.
    """

    class Genero(models.TextChoices):
        """Enumeración para el campo género."""
        MASCULINO = 'M', _('Masculino')
        FEMENINO = 'F', _('Femenino')
        OTRO = 'O', _('Otro')

    # Relación OneToOne con el modelo User.
    # on_delete=models.CASCADE significa que si se borra el User, se borra la Persona.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona')

    # --- CAMPOS ACTUALIZADOS ---
    # Hacemos que los campos principales sean opcionales (null=True, blank=True)
    # para permitir un registro simplificado.

    nombre = models.CharField(
        max_length=30,
        verbose_name=_('Nombre'),
        help_text=_('Nombre(s) de la persona.'),
        null=True, blank=True  # <-- CAMBIO
    )
    apellido = models.CharField(
        max_length=30,
        verbose_name=_('Apellido'),
        help_text=_('Apellido(s) de la persona.'),
        null=True, blank=True  # <-- CAMBIO
    )
    genero = models.CharField(
        max_length=1,
        choices=Genero.choices,
        verbose_name=_('Género'),
        help_text=_('Género de la persona.'),
        null=True, blank=True  # <-- CAMBIO
    )
    fecha_nacimiento = models.DateField(
        verbose_name=_('Fecha de Nacimiento'),
        help_text=_('Fecha de nacimiento de la persona.'),
        null=True, blank=True  # <-- CAMBIO
    )

    # --- FIN DE CAMPOS ACTUALIZADOS ---

    # Estos campos ya eran opcionales, los dejamos igual
    direccion = models.CharField(
        max_length=50,
        verbose_name=_('Dirección'),
        help_text=_('Dirección de residencia.'),
        blank=True, null=True
    )
    celular = models.CharField(
        max_length=15,
        verbose_name=_('Celular'),
        help_text=_('Número de teléfono celular.'),
        blank=True, null=True
    )

    # Campo booleano para el estado del usuario (activo/inactivo)
    estado = models.BooleanField(
        default=True,
        verbose_name=_('Estado'),
        help_text=_('Indica si el usuario está activo.')
    )

    # Campos de auditoría
    creado_en = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creado en')
    )
    actualizado_en = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Actualizado en')
    )

    class Meta:
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
        ordering = ['user__username']  # Ordenar por nombre de usuario

    def __str__(self):
        """
        Representación en cadena del modelo.
        """
        # Muestra el username del User si el nombre está vacío
        if self.nombre and self.apellido:
            return f"{self.nombre} {self.apellido} ({self.user.username})"
        return self.user.username