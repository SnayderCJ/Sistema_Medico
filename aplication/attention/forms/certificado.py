from django.forms import ModelForm, ValidationError
from django import forms
from aplication.attention.models import Certificado
from django.utils.timezone import now

# Definición de la clase CertificadoForm que hereda de ModelForm
class CertificadoForm(ModelForm):
    class Meta:
        model = Certificado
        fields = ["paciente", "doctor", "tipo_certificado", "observaciones"]

        # Personalización de los widgets para el formulario de Certificado
        widgets = {
            "paciente": forms.Select(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "doctor": forms.Select(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                }
            ),
            "tipo_certificado": forms.TextInput(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "placeholder": "Tipo de certificado (Ej. Certificado médico)"
                }
            ),
            "observaciones": forms.Textarea(
                attrs={
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
                    "rows": "4",
                    "placeholder": "Escriba las observaciones (opcional)"
                }
            ),
        }

    # Método de limpieza para validar el tipo de certificado
    def clean_tipo_certificado(self):
        tipo_certificado = self.cleaned_data.get("tipo_certificado")
        if not tipo_certificado:
            raise ValidationError("Debe ingresar el tipo de certificado.")
        return tipo_certificado

    # Método de limpieza para validar las observaciones (puede ser opcional)
    def clean_observaciones(self):
        observaciones = self.cleaned_data.get("observaciones")
        # Validación opcional: si se ingresan observaciones, que no sean muy cortas
        if observaciones and len(observaciones) < 10:
            raise ValidationError("Las observaciones deben tener al menos 10 caracteres.")
        return observaciones
