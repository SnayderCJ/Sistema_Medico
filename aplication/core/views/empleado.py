from django.urls import reverse_lazy
from aplication.core.forms.empleado import EmpleadoForm
from aplication.core.models import Empleado
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class EmpleadoListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/empleado/list.html"
    model = Empleado
    context_object_name = 'empleados'
    query = None
    paginate_by = 2
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')
        status = self.request.GET.get('status')
        
        if q1 is not None:
            self.query.add(Q(nombres__icontains=q1), Q.OR)
            
        if status == "activo":
            self.query.add(Q(activo=True), Q.AND)
        elif status == "inactivo":
            self.query.add(Q(activo=False), Q.AND)
        return self.model.objects.filter(self.query).order_by('activo')
    
class EmpleadoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Empleado
    template_name = 'core/empleado/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Grabar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        empleado = self.object
        save_audit(self.request, empleado, action='A')
        messages.success(self.request, f"Éxito al crear el empleado {empleado.nombre_completo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Empleado
    template_name = 'core/empleado/form.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Actualizar Empleado'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        empleado = self.object
        save_audit(self.request, empleado, action='M')
        messages.success(self.request, f"Éxito al modificar el empleado {empleado.nombre_completo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Empleado
    success_url = reverse_lazy('core:empleado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grabar'] = 'Eliminar Empleado'
        context['description'] = f"¿Desea eliminar el empleado: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el empleado {self.object.nombre_completo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class EmpleadoDetailView(LoginRequiredMixin,DetailView):
    model = Empleado

    def get(self, request, *args, **kwargs):
        empleado = self.get_object()
        data = {
            'id': empleado.id,
            'nombres': empleado.nombres,
            'apellidos': empleado.apellidos,
            'dni': empleado.cedula,
            'direccion': empleado.direccion,
            'foto': empleado.get_image(),
            'fecha_nacimiento': empleado.fecha_nacimiento,
            'edad': empleado.calcular_edad(empleado.fecha_nacimiento),
            'cargo': empleado.cargo.nombre,
            'sueldo': empleado.sueldo,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)
