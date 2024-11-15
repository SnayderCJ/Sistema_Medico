from django.urls import reverse_lazy
from aplication.core.forms.marcaMedicamento import MarcaMedicamentoForm
from aplication.core.models import MarcaMedicamento
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class MarcaMedicamentoListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/marcaMedicamento/list.html"
    model = MarcaMedicamento
    context_object_name = 'marcaMedicamentos'
    query = None
    paginate_by = 10
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q') # ver
        
        if q1 is not None: 
            self.query.add(Q(nombre__icontains=q1), Q.AND)   
        return self.model.objects.filter(self.query).order_by('nombre')
    
    
class MarcaMedicamentoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = MarcaMedicamento
    template_name = 'core/marcaMedicamento/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marcaMedicamento_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Marca'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        marca = self.object
        save_audit(self.request, marca, action='A')
        messages.success(self.request, f"Éxito al crear la marca {marca.nombre}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class MarcaMedicamentoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = MarcaMedicamento
    template_name = 'core/marcaMedicamento/form.html'
    form_class = MarcaMedicamentoForm
    success_url = reverse_lazy('core:marcaMedicamento_list')
    # permission_required = 'change_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Marcas'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        patient = self.object
        save_audit(self.request, patient, action='M')
        messages.success(self.request, f"Éxito al Modificar la Marca {patient.nombre}.")
        print("mande mensaje")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al Modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class MarcaMedicamentoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = MarcaMedicamento
    # template_name = 'core/patient/form.html'
    success_url = reverse_lazy('core:marcaMedicamento_list')
    # permission_required = 'delete_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Marca'
        context['description'] = f"¿Desea Eliminar la marca: {self.object.name}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente la marca {self.object.name}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
    
class MarcaMedicamentoDetailView(LoginRequiredMixin, DetailView):
    model = MarcaMedicamento
    
    def get(self, request, *args, **kwargs):
        marcaMedicamento = self.get_object()
        data = {
            'id': marcaMedicamento.id,
            'nombre': marcaMedicamento.nombre,
            'descripcion': marcaMedicamento.descripcion,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)