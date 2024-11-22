from django import forms
from aplication.attention.models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['paciente', 'metodo_pago']
        labels = {
            'paciente': 'Paciente',
            'metodo_pago': 'Método de Pago',
        }
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control', 'id': 'paciente-select'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }

    costos = forms.CharField(
        widget=forms.Textarea(attrs={'readonly': 'readonly', 'class': 'form-control', 'rows': 5}),
        required=False,
        label='Costos Detallados'
    )
