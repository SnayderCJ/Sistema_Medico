from django import forms
from aplication.attention.models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['paciente', 'costo_atencion', 'servicios_adicionales', 'examenes_medicos', 'metodo_pago']
        labels = {
            'paciente': 'Paciente',
            'costo_atencion': 'Costo Atención',
            'servicios_adicionales': 'Servicios Adicionales',
            'examenes_medicos': 'Exámenes Médicos',
            'metodo_pago': 'Método de Pago',
        }
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'costo_atencion': forms.Select(attrs={'class': 'form-control'}),
            'servicios_adicionales': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'examenes_medicos': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }

def clean(self):
        cleaned_data = super().clean()
        servicios_adicionales = cleaned_data.get('servicios_adicionales')
        examenes_medicos = cleaned_data.get('examenes_medicos')

        # Validar que al menos uno de los dos campos no esté vacío
        if not servicios_adicionales and not examenes_medicos:
            raise forms.ValidationError("Debe seleccionar al menos un servicio adicional o un examen médico.")

        return cleaned_data