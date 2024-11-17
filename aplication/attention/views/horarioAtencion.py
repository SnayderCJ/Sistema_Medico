from django.urls import reverse_lazy
from aplication.attention.forms.horarioAtencion import HorarioAtencionForm
from aplication.attention.models import HorarioAtencion
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.utils import save_audit

class HorarioAtencionListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "attention/horarioAtencion/list.html"
    model = HorarioAtencion
    context_object_name = 'horarios'
    query = None
    paginate_by = 10
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q') # ver
        status = self.request.GET.get('status')
        
        if q1 is not None: 
            self.query.add(Q(dia_semana__icontains=q1), Q.AND)
        
        if status == "activo":
            self.query.add(Q(activo=True), Q.AND)
        elif status == "inactivo":
            self.query.add(Q(activo=False), Q.AND)
        return self.model.objects.filter(self.query).order_by('activo')
    
    
class HorarioAtencionCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = HorarioAtencion
    template_name = 'attention/horarioAtencion/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('attention:horario_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Horario'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        # print("entro al form_valid")
        response = super().form_valid(form)
        horario = self.object
        save_audit(self.request, horario, action='A')
        messages.success(self.request, f"Éxito al crear el horario {horario.dia_semana}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class HorarioAtencionUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = HorarioAtencion
    template_name = 'attention/horarioAtencion/form.html'
    form_class = HorarioAtencionForm
    success_url = reverse_lazy('attention:horario_list')
    # permission_required = 'change_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar horario'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        horario = self.object
        save_audit(self.request, horario, action='M')
        messages.success(self.request, f"Éxito al Modificar el horario {horario.dia_semana}.")
        print("mande mensaje")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al Modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class HorarioAtencionDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = HorarioAtencion
    # template_name = 'core/patient/form.html'
    success_url = reverse_lazy('attention:horario_list')
    # permission_required = 'delete_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar horario'
        context['description'] = f"¿Desea Eliminar el horario: {self.object.dia_semana}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el horario {self.object.dia_semana}."
        messages.success(self.request, success_message)
        # Cambiar el estado de eliminado lógico
        # self.object.deleted = True
        # self.object.save()
        return super().delete(request, *args, **kwargs)
    
class HorarioAtencionDetailView(LoginRequiredMixin,DetailView):
    model = HorarioAtencion
    
    def get(self, request, *args, **kwargs):
        horario = self.get_object()
        data = {
            'id': horario.id,
            'dia_semana': horario.dia_semana,
            'hora_inicio': horario.hora_inicio,
            'hora_fin': horario.hora_fin,
            'Intervalo_desde': horario.Intervalo_desde,
            'Intervalo_hasta': horario.Intervalo_hasta,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)