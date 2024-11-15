from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import TipoSangre

# Definición de la clase TipoSangreForm que hereda de ModelForm
class TipoSangreForm(ModelForm):
    # Clase interna Meta para configurar el formulario
    class Meta:    
        model = TipoSangre
        # campos que se muestran en este mismo orden en el formulario como etiquetas html
        fields = ['tipo', 'descripcion']
     
        # Mensajes de error personalizados para ciertos campos
        error_messages = {
            "tipo": {
                "unique": "Ya existe un tipo de sangre con este nombre.",
            },
        }
     
        # Personalización de los widgets o etiquetas que se van a mostrar en el formulario html si no se desea el valor por default dado en el modelo
        widgets = {
            "tipo": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese tipo de sangre",
                    "id": "id_tipo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese descripción",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
        }
        labels = {
            "tipo": "Tipo de Sangre",
            "descripcion": "Descripción",
        }

    # método de limpieza se ejecuta automáticamente cuando Django valida el campo tipo en el formulario al ejecutar el metodo form_valid()
    def clean_tipo(self):
        tipo = self.cleaned_data.get("tipo")
        # Verificar si el campo tiene menos de 1 carácter
        if not tipo or len(tipo) < 1:
            raise ValidationError("El tipo de sangre debe tener al menos 1 carácter.")
        
        return tipo.upper()

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get("descripcion")
        # Verificar si el campo tiene menos de 1 carácter
        if not descripcion or len(descripcion) < 1:
            raise ValidationError("La descripción debe tener al menos 1 carácter.")

        return descripcion.upper()
