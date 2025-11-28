from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Persona


# --- 1. FORMULARIO DE REGISTRO ---
class UserForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'reg_password'  # <--- ID CRÍTICO PARA EL JS
        })
    )
    password_confirm = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar Contraseña',
            'id': 'reg_confirm'  # <--- ID CRÍTICO PARA EL JS
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# --- 2. FORMULARIO DE LOGIN ---
class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Usuario'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'login_password'  # <--- ID CRÍTICO PARA EL JS
        })


# --- 3. OTROS FORMULARIOS (Perfil, etc) ---
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        exclude = ('user', 'estado', 'creado_en', 'actualizado_en', 'rol')
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class PersonaAdminForm(forms.ModelForm):
    """
    Formulario exclusivo para administradores.
    Permite cambiar el ROL y el ESTADO de un usuario.
    """

    class Meta:
        model = Persona
        fields = ['rol', 'estado']
        widgets = {
            'rol': forms.Select(attrs={'class': 'form-control'}),
            # Checkbox estilizado (dependiendo de tu CSS, o simple checkbox)
            'estado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
