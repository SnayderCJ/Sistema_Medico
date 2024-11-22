from django import forms
from aplication.attention.models import Pago, ServiciosAdicionales, ExamenSolicitado


class PagoForm(forms.ModelForm):
    servicios_adicionales = forms.ModelMultipleChoiceField(
        queryset=ServiciosAdicionales.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )
    examenes_medicos = forms.ModelMultipleChoiceField(
        queryset=ExamenSolicitado.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
    )

    class Meta:
        model = Pago
        fields = ['paciente', 'costo_atencion', 'metodo_pago', 'servicios_adicionales', 'examenes_medicos']
        labels = {
            'paciente': 'Paciente',
            'costo_atencion': 'Costo Atención',
            'metodo_pago': 'Método de Pago',
            'servicios_adicionales': 'Servicios Adicionales',
            'examenes_medicos': 'Exámenes Médicos',
        }
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'costo_atencion': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si necesitas filtrar los servicios adicionales o exámenes médicos por paciente o atención, 
        # puedes hacerlo aquí. Por ejemplo:
        # if 'paciente' in self.initial:
        #     paciente = self.initial['paciente']
        #     self.fields['servicios_adicionales'].queryset = ServiciosAdicionales.objects.filter(
        #         # ... filtro por paciente
        #     )
        #     self.fields['examenes_medicos'].queryset = ExamenSolicitado.objects.filter(
        #         # ... filtro por paciente
        #     )

    def clean(self):
        cleaned_data = super().clean()
        servicios_adicionales = cleaned_data.get('servicios_adicionales')
        examenes_medicos = cleaned_data.get('examenes_medicos')

        # Validar que al menos uno de los dos campos no esté vacío
        if not servicios_adicionales and not examenes_medicos:
            raise forms.ValidationError("Debe seleccionar al menos un servicio adicional o un examen médico.")

        return cleaned_data