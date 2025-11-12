from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Persona(models.Model):
    """
    Modelo que extiende el User de Django con una relación 1 a 1
    para almacenar datos adicionales de una persona.
    """

    # Opciones para el campo 'genero'
    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    # --- Relación Uno a Uno ---
    # Si se elimina el User, se elimina la Persona asociada
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='persona')

    # --- Campos de la tabla ---
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)

    # Usamos 'choices' para limitar las opciones de género
    genero = models.CharField(max_length=25, choices=GENERO_OPCIONES)

    fecha_nacimiento = models.DateField()

    # 'default=True' para que las personas estén activas por defecto
    estado = models.BooleanField(default=True)

    # 'blank=True' y 'null=True' hacen que estos campos no sean obligatorios
    direccion = models.CharField(max_length=50, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)

    # Campos automáticos de auditoría
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Muestra el nombre completo en el admin de Django
        return f"{self.nombre} {self.apellido} ({self.user.username})"

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
