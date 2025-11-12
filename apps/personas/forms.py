from django import forms
from django.contrib.auth.models import User
from .models import Persona


class UserForm(forms.ModelForm):
    """
    Formulario para el modelo User de Django.
    Se usa en el registro simplificado.
    """
    # --- AÑADIMOS EL CAMPO DE CONFIRMACIÓN ---
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirmar Contraseña'}
        )
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Contraseña'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }
        labels = {
            'username': 'Usuario',
            'email': 'Email',
        }

    # --- AÑADIMOS LA LÓGICA DE VALIDACIÓN ---
    def clean(self):
        """
        Sobrescribimos el método clean para validar que
        las contraseñas coincidan.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            # Si no coinciden, lanzamos un error de validación
            self.add_error('password_confirm', "Las contraseñas no coinciden.")

        return cleaned_data


class PersonaForm(forms.ModelForm):
    """
    Formulario para el modelo Persona.
    Se usa en la VISTA DE EDICIÓN de perfil.
    """
    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Fecha de Nacimiento (YYYY-MM-DD)',
                'type': 'date'  # Para que muestre un calendario
            }
        ),
        # Marcamos como no requerido (ya que el modelo lo permite)
        required=False
    )

    class Meta:
        model = Persona
        # Excluimos los campos que no debe llenar el usuario
        exclude = ('user', 'estado', 'creado_en', 'actualizado_en')

        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Apellido'}),
            'genero': forms.Select(attrs={'class': 'no-icon'}),  # 'no-icon' para alinear el CSS
            'direccion': forms.TextInput(attrs={'placeholder': 'Dirección (Opcional)'}),
            'celular': forms.TextInput(attrs={'placeholder': 'Celular (Opcional)'}),
        }
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'genero': 'Género',
            'direccion': 'Dirección',
            'celular': 'Celular',
        }


class UserEditForm(forms.ModelForm):
    """
    Formulario para EDITAR el User (sin contraseña).
    Se usa en la VISTA DE EDICIÓN de perfil.
    """

    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
        }