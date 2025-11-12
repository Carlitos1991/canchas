from django import forms
from django.contrib.auth.models import User
from .models import Persona


class UserForm(forms.ModelForm):
    """
    Formulario para la creación de un User (registro).
    """
    # Hacemos que 'password' sea un PasswordInput
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        # Ya no necesitamos widgets para añadir clases


class UserEditForm(forms.ModelForm):
    """
    Formulario para editar los datos básicos del User (email y username).
    """

    class Meta:
        model = User
        fields = ['username', 'email']
        # Ya no necesitamos widgets


class PersonaForm(forms.ModelForm):
    """
    Formulario para los datos del modelo Persona.
    """

    # Opciones de Género
    GENERO_CHOICES = [
        ('', 'Selecciona tu género'),
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    # Sobreescribimos el campo genero para usar 'choices'
    genero = forms.ChoiceField(choices=GENERO_CHOICES)

    # Hacemos que 'fecha_nacimiento' sea un DateInput
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'genero', 'fecha_nacimiento', 'estado', 'direccion', 'celular']
        # Quitamos todos los widgets que ponían clases de Tailwind
        widgets = {
            'estado': forms.CheckboxInput(),  # Usar un checkbox simple
        }