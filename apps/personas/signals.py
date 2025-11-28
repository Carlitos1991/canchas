from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Persona

@receiver(post_save, sender=Persona)
def asignar_grupo_a_usuario(sender, instance, created, **kwargs):
    """
    Asigna un usuario a un grupo basado en su rol en el modelo Persona.
    Se ejecuta después de que se guarda una instancia de Persona.
    """
    if instance.rol == Persona.Rol.EMPRESARIO:
        grupo, _ = Group.objects.get_or_create(name='Empresarios')
        instance.user.groups.add(grupo)
    elif instance.rol == Persona.Rol.CLIENTE:
        grupo, _ = Group.objects.get_or_create(name='Clientes')
        instance.user.groups.add(grupo)
