from django import forms
from .models import RegistroSemanal, Conductor
from django.forms.widgets import DateInput

class RegistroSemanalForm(forms.ModelForm):
    class Meta:
        model = RegistroSemanal
        fields = ['conductor', 'semana', 'año', 'entregado', 'fecha_entrega']
        widgets = {
            'fecha_entrega': DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            )
        }
        labels = {
            'conductor': 'Conductor',
            'semana': 'Semana',
            'año': 'Año',
            'entregado': 'Entregado',
            'fecha_entrega': 'Fecha de Entrega'
        }
        
class ConductorForm(forms.ModelForm):
    class Meta:
        model = Conductor
        fields = ['nombre', 'rut']
        labels = {
            'nombre': 'Nombre del Conductor',
            'rut': 'RUT'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'juan Perez'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12.345.678-9'})
        }        