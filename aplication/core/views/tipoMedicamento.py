from django.urls import reverse_lazy
from aplication.core.forms.tipoMedicamento import TipoMedicamentoForm
from aplication.core.models import TipoMedicamento
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class TipoMedicamentoListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/tipoMedicamento/list.html"
    model = TipoMedicamento
    context_object_name = 'tipo_medicamentos'
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
    
    
class TipoMedicamentoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = TipoMedicamento
    template_name = 'core/tipoMedicamento/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipoMedicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Tipo de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_medicamento = self.object
        save_audit(self.request, tipo_medicamento, action='A')
        messages.success(self.request, f"Éxito al crear el tipo de medicamento {tipo_medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class TipoMedicamentoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = TipoMedicamento
    template_name = 'core/tipoMedicamento/form.html'
    form_class = TipoMedicamentoForm
    success_url = reverse_lazy('core:tipoMedicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Tipo de Medicamento'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_medicamento = self.object
        save_audit(self.request, tipo_medicamento, action='M')
        messages.success(self.request, f"Éxito al modificar el tipo de medicamento {tipo_medicamento.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class TipoMedicamentoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = TipoMedicamento
    success_url = reverse_lazy('core:tipoMedicamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Tipo de Medicamento'
        context['description'] = f"¿Desea eliminar el tipo de medicamento: {self.object.nombre}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el tipo de medicamento {self.object.nombre}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class TipoMedicamentoDetailView(LoginRequiredMixin,DetailView):
    model = TipoMedicamento

    def get(self, request, *args, **kwargs):
        tipo_medicamento = self.get_object()
        data = {
            'id': tipo_medicamento.id,
            'nombre': tipo_medicamento.nombre,
            'descripcion': tipo_medicamento.descripcion,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)