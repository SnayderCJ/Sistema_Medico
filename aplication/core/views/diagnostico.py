from django.urls import reverse_lazy
from aplication.core.forms.diagnostico import DiagnosticoForm
from aplication.core.models import Diagnostico
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class DiagnosticoListView(LoginRequiredMixin,ListViewMixin,ListView):
   template_name = "core/diagnostico/list.html"
   model = Diagnostico
   context_object_name = 'diagnosticos'
   paginate_by = 10
    
   def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q') # ver
        status = self.request.GET.get('status')
        
        if q1 is not None:
            self.query.add(Q(activo__icontains=q1), Q.OR)
            
        if status == "activo":
            self.query.add(Q(activo=True), Q.AND)
        elif status == "inactivo":
            self.query.add(Q(activo=False), Q.AND)
        return self.model.objects.filter(self.query).order_by('activo')

    
class DiagnosticoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Diagnostico'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        # print("entro al form_valid")
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='A')
        messages.success(self.request, f"Éxito al crear al diagnostico {diagnostico.codigo}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class DiagnosticoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Diagnostico
    template_name = 'core/diagnostico/form.html'
    form_class = DiagnosticoForm
    success_url = reverse_lazy('core:diagnostico_list')
    # permission_required = 'change_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar diagnostico'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        diagnostico = self.object
        save_audit(self.request, diagnostico, action='M')
        messages.success(self.request, f"Éxito al Modificar el diagnostico {diagnostico.codigo}.")
        print("mande mensaje")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al Modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class DiagnosticoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Diagnostico
    success_url = reverse_lazy('core:diagnostico_list')
    # permission_required = 'delete_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar diagnostico'
        context['description'] = f"¿Desea Eliminar al diagnostico: {self.object.name}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el diagnostico {self.object.name}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
    
class DiagnosticoDetailView(LoginRequiredMixin, DetailView):
    model = Diagnostico
    
    def get(self, request, *args, **kwargs):
        diagnostico = self.get_object()
        data = {
            'id': diagnostico.id,
            'codigo': diagnostico.codigo,
            'descripcion': diagnostico.descripcion,
            'datos_adicionales': diagnostico.datos_adicionales,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)