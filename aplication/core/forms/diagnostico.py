from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Diagnostico

# Definición de la clase PatientForm que hereda de ModelForm
class DiagnosticoForm(ModelForm):
        # Clase interna Meta para configurar el formulario
    class Meta:    
        model = Diagnostico
        # campos que se muestran en este mismo orden en el formulario como etiquetas html
        fields = ["codigo","descripcion","datos_adicionales","activo"]
     
        # Mensajes de error personalizados para ciertos campos
        error_messages = {
            "codigo": {
                "unique": "Ya existe un diagnostico con ese codigo.",
            },
        }
     
        # Personalización de los widgets o etiquetas que se van a mostrar en el formulario html si no se desea el valor por default dado en el modelo
        widgets = {
            "codigo": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese codigo",
                    "id": "id_codigo",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "descripcion": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese descripcion",
                    "id": "id_descripcion",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "datos_adicionales": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese datos adicionales",
                    "id": "id_datos_adicionales",
                    "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
                }
            ),
            "activo": forms.CheckboxInput(
                attrs={
                    "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                }
            ),
        }

