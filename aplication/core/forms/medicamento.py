from django.forms import ModelForm, ValidationError
from django import forms
from aplication.core.models import Medicamento

# Definición de la clase MedicamentoForm que hereda de ModelForm
class MedicamentoForm(ModelForm):
    # Clase interna Meta para configurar el formulario
    class Meta:    
        model = Medicamento
        # campos que se muestran en este mismo orden en el formulario como etiquetas html
        fields = ["nombre", "descripcion", "precio", "concentracion", "foto", "tipo", "marca_medicamento", "cantidad", "comercial", "activo"]
     
        # Mensajes de error personalizados para ciertos campos
        error_messages = {
            "nombre": {
            "unique": "Ya existe un medicamento con este nombre",
            },
        }
         
        # Personalización de los widgets o etiquetas que se van a mostrar en el formulario html si no se desea el valor por default dado en el modelo
        widgets = {
            "nombre": forms.TextInput(
            attrs={
                "placeholder": "Ingrese nombre del medicamento",
                "id": "id_nombre",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "descripcion": forms.Textarea(
            attrs={
                "placeholder": "Ingrese descripción del medicamento",
                "id": "id_descripcion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "precio": forms.NumberInput(
            attrs={
                "placeholder": "Ingrese precio del medicamento",
                "id": "id_precio",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "concentracion": forms.TextInput(
            attrs={
                "placeholder": "Ingrese concentración del medicamento",
                "id": "id_concentracion",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "foto": forms.ClearableFileInput(
            attrs={
                "id": "id_foto",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "tipo": forms.Select(
            attrs={
                "id": "id_tipo",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "marca_medicamento": forms.Select(
            attrs={
                "placeholder": "Ingrese marca del medicamento",
                "id": "id_marca_medicamento",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "cantidad": forms.NumberInput(
            attrs={
                "placeholder": "Ingrese cantidad disponible",
                "id": "id_cantidad",
                "class": "shadow-sm bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 pr-12 dark:bg-principal dark:border-gray-600 dark:placeholder-gray-400 dark:text-gray-400 dark:focus:ring-blue-500 dark:focus:border-blue-500 dark:shadow-sm-light",
            }
            ),
            "comercial": forms.CheckboxInput(
            attrs={
                "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            }
            ),
            "activo": forms.CheckboxInput(
            attrs={
                "class": "mt-1 block px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            }
            ),
        }
        labels = {
            "nombre": "Nombre del Medicamento",
        }

# método de limpieza se ejecuta automáticamente cuando Django valida el campo nombre en el formulario al ejecutar el metodo form_valid()
def clean_nombre(self):
    nombre = self.cleaned_data.get("nombre")
    # Verificar si el campo tiene menos de 1 carácter
    if not nombre or len(nombre) < 2:
        raise ValidationError("El nombre debe tener al menos 2 caracteres.")
    
    return nombre.upper()

def clean_descripcion(self):
    descripcion = self.cleaned_data.get("descripcion")
    # Verificar si el campo tiene menos de 1 carácter
    if not descripcion or len(descripcion) < 10:
        raise ValidationError("La descripción debe tener al menos 10 caracteres.")

    return descripcion

def clean_precio(self):
    precio = self.cleaned_data.get("precio")
    # Verificar si el precio es mayor que 0
    if precio <= 0:
        raise ValidationError("El precio debe ser mayor que 0.")
    
    return precio

def clean_cantidad(self):
    cantidad = self.cleaned_data.get("cantidad")
    # Verificar si la cantidad es mayor que 0
    if cantidad <= 0:
        raise ValidationError("La cantidad debe ser mayor que 0.")
    
    return cantidad