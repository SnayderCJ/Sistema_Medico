from django.forms import ModelForm, ValidationError
from django import forms
from aplication.attention.models import CitaMedica

# Definición de la clase CitaMedicaForm que hereda de ModelForm
class CitaMedicaForm(ModelForm):
    class Meta:
        model = CitaMedica
        fields = ["paciente", "fecha", "hora_cita", "estado"]
     
        # Personalización de los widgets para el formulario de CitaMedica
        widgets = {
            "paciente": forms.Select(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "fecha": forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    "placeholder": "Fecha de la cita (YYYY-MM-DD)",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "type": "date",
                }
            ),
            "hora_cita": forms.TimeInput(
                format='%H:%M',
                attrs={
                    "placeholder": "Hora de la cita (HH:MM)",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "type": "time",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
        }

    # Método de limpieza para validar la hora de la cita
    def clean_hora_cita(self):
        hora_cita = self.cleaned_data.get("hora_cita")
        # Validación personalizada de la hora de la cita
        if not hora_cita:
            raise ValidationError("Debe ingresar una hora para la cita.")
        
        return hora_cita