from django.urls import reverse_lazy
from aplication.attention.forms.examenSolicitado import ExamenSolicitadoForm
from aplication.attention.models import ExamenSolicitado
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.utils import save_audit

class ExamenSolicitadoListView(LoginRequiredMixin, ListViewMixin, ListView):
   template_name = "attention/examenSolicitado/list.html"
   model = ExamenSolicitado
   context_object_name = 'examenes'
   query = None
   paginate_by = 10

   def get_queryset(self):
      self.query = Q()
      q1 = self.request.GET.get('q')
      estado = self.request.GET.get('estado')
      
      if q1 is not None:
         self.query &= Q(nombre_examen__icontains=q1)
      if estado == "S":
         self.query &= Q(estado='S')
      elif estado == "R":
          self.query &= Q(estado='R')

      return self.model.objects.filter(self.query).order_by('-fecha_solicitud')


class ExamenSolicitadoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
   model = ExamenSolicitado
   template_name = 'attention/examenSolicitado/form.html'
   form_class = ExamenSolicitadoForm
   success_url = reverse_lazy('attention:examen_list')

   def get_context_data(self, **kwargs):
      context = super().get_context_data()
      context['grabar'] = 'Grabar examen'
      context['back_url'] = self.success_url
      return context

   def form_valid(self, form):
      response = super().form_valid(form)
      examen = self.object
      save_audit(self.request, examen, action='A')
      messages.success(self.request, f"Éxito al crear el examen {examen.nombre_examen}.")
      return response

   def form_invalid(self, form):
      messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
      print(form.errors)
      return self.render_to_response(self.get_context_data(form=form))


class ExamenSolicitadoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
   model = ExamenSolicitado
   template_name = 'attention/examenSolicitado/form.html'
   form_class = ExamenSolicitadoForm
   success_url = reverse_lazy('attention:examen_list')

   def get_context_data(self, **kwargs):
      context = super().get_context_data()
      context['grabar'] = 'Actualizar examen'
      context['back_url'] = self.success_url
      return context

   def form_valid(self, form):
      response = super().form_valid(form)
      examen = self.object
      save_audit(self.request, examen, action='M')
      messages.success(self.request, f"Éxito al modificar el examen {examen.nombre_examen}.")
      return response

   def form_invalid(self, form):
      messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
      print(form.errors)
      return self.render_to_response(self.get_context_data(form=form))


class ExamenSolicitadoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
   model = ExamenSolicitado
   success_url = reverse_lazy('attention:examen_list')

   def get_context_data(self, **kwargs):
      context = super().get_context_data()
      context['grabar'] = 'Eliminar examen'
      context['description'] = f"¿Desea eliminar el examen: {self.object.nombre_examen}?"
      context['back_url'] = self.success_url
      return context

   def delete(self, request, *args, **kwargs):
      self.object = self.get_object()
      success_message = f"Éxito al eliminar lógicamente el examen {self.object.nombre_examen}."
      messages.success(self.request, success_message)
      return super().delete(request, *args, **kwargs)


class ExamenSolicitadoDetailView(LoginRequiredMixin, DetailView):
   model = ExamenSolicitado

   def get(self, request, *args, **kwargs):
      examen = self.get_object()
      data = {
         'id': examen.id,
         'paciente': str(examen.paciente),
         'nombre_examen': examen.nombre_examen,
         'costo': examen.costo,
         'fecha_solicitud': str(examen.fecha_solicitud),
         'resultado_archivo': examen.resultado.url if examen.resultado else None,
         'comentario': examen.comentario, 
         # Añade más campos según tu modelo
      }
      return JsonResponse(data)
