from django.forms import ModelForm, ValidationError
from django import forms
from aplication.attention.models import ExamenSolicitado

class ExamenSolicitadoForm(ModelForm):
   class Meta:
      model = ExamenSolicitado
      fields = ["nombre_examen", "paciente", "costo", "resultado", "comentario", "estado"]
      
      widgets = {
         "nombre_examen": forms.TextInput(
            attrs={
               "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
            }
         ),
         "paciente": forms.Select(
            attrs={
               "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
            }
         ),
         "costo": forms.NumberInput(
            attrs={
               "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
            }
         ),
         "resultado": forms.ClearableFileInput(
            attrs={
               "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
            }
         ),
         "comentario": forms.Textarea(
            attrs={
               "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
               "rows": 3,
            }
         ),
         "estado": forms.Select(
            attrs={
               "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5",
            }
         ),
      }

   def clean_costo(self):
      costo = self.cleaned_data.get("costo")
      if costo <= 0:
         raise ValidationError("El costo debe ser un valor positivo.")
      return costo
