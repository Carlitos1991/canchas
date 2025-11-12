from django import forms
from django.contrib.auth.models import User
from .models import Persona


class UserForm(forms.ModelForm):
    """
    Formulario para el modelo User de Django.
    Se usa en el registro.
    """
    # Sobrescribimos el campo password para usar PasswordInput
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña'}  # Placeholder para el nuevo diseño
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # Añadimos widgets para los placeholders
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }


class PersonaForm(forms.ModelForm):
    """
    Formulario para el modelo Persona.
    Se usa en el registro.
    """
    # Hacemos que la fecha sea un Input de tipo "text" para el placeholder
    # y le pedimos al navegador que muestre un Date Picker si puede
    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Fecha de Nacimiento (YYYY-MM-DD)',
                'type': 'date'  # HTML5 date picker
            }
        )
    )

    class Meta:
        model = Persona
        # Excluimos los campos que no debe llenar el usuario
        exclude = ('user', 'estado', 'creado_en', 'actualizado_en')

        # Añadimos placeholders para el nuevo diseño
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'genero': forms.Select(attrs={'class': 'no-icon'}),  # 'no-icon' para alinear el padding
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección (Opcional)'}),
            'celular': forms.TextInput(attrs={'placeholder': 'Celular (Opcional)'}),
        }


class UserEditForm(forms.ModelForm):
    """
    Formulario para EDITAR el User.
    No se puede editar la contraseña desde aquí.
    """

    class Meta:
        model = User
        fields = ('username', 'email')  # Solo estos campos