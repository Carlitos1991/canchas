from django import forms
from django.contrib.auth.models import User
from .models import Persona


class UserForm(forms.ModelForm):
    """
    Formulario para crear el User (autenticación).
    Usamos un PasswordInput para ocultar la contraseña.
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PersonaForm(forms.ModelForm):
    """
    Formulario para crear la Persona (datos de perfil).
    Usamos un DateInput para el calendario.
    """
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de Nacimiento"
    )

    class Meta:
        model = Persona
        # Excluimos 'user' porque se asignará en la vista
        # Excluimos 'estado' porque tiene un valor por defecto
        exclude = ['user', 'estado', 'creado_en', 'actualizado_en']