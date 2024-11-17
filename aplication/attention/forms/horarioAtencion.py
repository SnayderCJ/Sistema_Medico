from django.forms import ModelForm, ValidationError
from django import forms
from aplication.attention.models import HorarioAtencion

# Definición de la clase HorarioAtencionForm que hereda de ModelForm
class HorarioAtencionForm(ModelForm):
    class Meta:    
        model = HorarioAtencion
        fields = ["dia_semana", "hora_inicio", "hora_fin", "Intervalo_desde", "Intervalo_hasta", "activo"]
     
        # Personalización de los widgets para el formulario de HorarioAtencion
        widgets = {
            "dia_semana": forms.Select(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "hora_inicio": forms.TimeInput(
                format='%H:%M',
                attrs={
                    "placeholder": "Hora de inicio",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "hora_fin": forms.TimeInput(
                format='%H:%M',
                attrs={
                    "placeholder": "Hora de fin",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "Intervalo_desde": forms.TimeInput(
                format='%H:%M',
                attrs={
                    "placeholder": "Intervalo desde",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "Intervalo_hasta": forms.TimeInput(
                format='%H:%M',
                attrs={
                    "placeholder": "Intervalo hasta",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "rounded focus:ring-blue-500 focus:border-blue-500",
                }
            ),
        }

    # Método de limpieza para validar hora de inicio y fin
    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")
        
        return cleaned_data