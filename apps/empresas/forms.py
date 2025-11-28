from django import forms
from .models import Empresa, Cancha, Disponibilidad

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'gerente', 'direccion', 'ubicacion_url', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Comercial'}),
            'gerente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del Gerente'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección Física'}),
            'ubicacion_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://maps.google.com/...'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        }

class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = ['nombre', 'capacidad', 'precio_hora']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Cancha 1'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 10'}),
            'precio_hora': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }

class DisponibilidadForm(forms.ModelForm):
    """
    Formulario para crear y editar horarios de disponibilidad.
    """
    class Meta:
        model = Disponibilidad
        fields = ['fecha', 'hora_inicio', 'hora_fin', 'estado']
        widgets = {
            # Usamos los widgets HTML5 para una mejor experiencia de usuario
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
