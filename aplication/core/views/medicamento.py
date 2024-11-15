from django.urls import reverse_lazy
from aplication.core.forms.medicamento import MedicamentoForm
from aplication.core.models import Medicamento
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class MedicamentoListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/medicamento/list.html"
    model = Medicamento
    context_object_name = 'medicamentos'
    query = None
    paginate_by = 2
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        if q1 is not None:
            self.query.add(Q(nombre__icontains=q1), Q.OR)
            
        if status == "activo":
            self.query.add(Q(activo=True), Q.AND)
        elif status == "inactivo":
            self.query.add(Q(activo=False), Q.AND)
        return self.model.objects.filter(self.query).order_by('activo')
    
    
class MedicamentoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Medicamento
    template_name = 'core/medicamento/form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        save_audit(self.request, medicamento, action='A')
        messages.success(self.request, f"Éxito al crear el medicamento {medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class MedicamentoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Medicamento
    template_name = 'medicamento/form.html'
    form_class = MedicamentoForm
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        medicamento = self.object
        save_audit(self.request, medicamento, action='M')
        messages.success(self.request, f"Éxito al modificar el medicamento {medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class MedicamentoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Medicamento
    success_url = reverse_lazy('core:medicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Medicamento'
        context['description'] = f"¿Desea eliminar el medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el medicamento {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class MedicamentoDetailView(LoginRequiredMixin, DetailView):
    model = Medicamento

    def get(self, request, *args, **kwargs):
        medicamento = self.get_object()
        data = {
            'id': medicamento.id,
            'nombre': medicamento.nombre,
            'descripcion': medicamento.descripcion,
            'concentracion': medicamento.concentracion,
            'tipo': medicamento.tipo.nombre,
            'marca_medicamento': medicamento.marca_medicamento.nombre,
            'cantidad': medicamento.cantidad,
            'precio': medicamento.precio,
            'foto': medicamento.get_image(),
            'comercial': medicamento.comercial,
            'activo': medicamento.activo,
        }
        return JsonResponse(data)
