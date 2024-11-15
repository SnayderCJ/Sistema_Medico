from django.urls import reverse_lazy
from aplication.core.forms.especialidad import EspecialidadForm
from aplication.core.models import Especialidad
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class EspecialidadListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/especialidad/list.html"
    model = Especialidad
    context_object_name = 'especialidades'
    query = None
    paginate_by = 2
    
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
    
class EspecialidadCreateView(LoginRequiredMixin,CreateViewMixin, CreateView):
    model = Especialidad
    template_name = 'core/especialidad/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        save_audit(self.request, especialidad, action='A')
        messages.success(self.request, f"Éxito al crear la especialidad {especialidad.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class EspecialidadUpdateView(LoginRequiredMixin,UpdateViewMixin,UpdateView):
    model = Especialidad
    template_name = 'core/especialidad/form.html'
    form_class = EspecialidadForm
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Especialidad'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        especialidad = self.object
        save_audit(self.request, especialidad, action='M')
        messages.success(self.request, f"Éxito al modificar la especialidad {especialidad.nombre}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))


class EspecialidadDeleteView(LoginRequiredMixin,DeleteViewMixin,DeleteView):
    model = Especialidad
    success_url = reverse_lazy('core:especialidad_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Especialidad'
        context['description'] = f"¿Desea eliminar la especialidad: {self.object.tipo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar la especialidad {self.object.tipo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)


class EspecialidadDetailView(LoginRequiredMixin,DetailView):
    model = Especialidad

    def get(self, request, *args, **kwargs):
        especialidad = self.get_object()
        data = {
            'id': especialidad.id,
            'nombre': especialidad.nombre,
            'descripcion': especialidad.descripcion,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)
