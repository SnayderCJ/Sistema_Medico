from django.urls import reverse_lazy
from aplication.core.forms.doctor import DoctorForm
from aplication.core.models import Doctor
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class DoctorListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/doctor/list.html"
    model = Doctor
    context_object_name = 'doctores'
    query = None
    paginate_by = 2
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q') # ver
        if q1 is not None: 
            self.query.add(Q(nombres__icontains=q1), Q.OR) 
            self.query.add(Q(apellidos__icontains=q1), Q.OR) 
            self.query.add(Q(activo__icontains=q1), Q.OR) 
        return self.model.objects.filter(self.query).order_by('apellidos')
    
class DoctorCreateView(LoginRequiredMixin,CreateViewMixin, CreateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')
    # permission_required = 'add_doctor' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Doctor'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        save_audit(self.request, doctor, action='A')
        messages.success(self.request, f"Éxito al crear al doctor {doctor.nombre_completo}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class DoctorUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Doctor
    template_name = 'core/doctor/form.html'
    form_class = DoctorForm
    success_url = reverse_lazy('core:doctor_list')
    # permission_required = 'change_doctor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Doctor'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        doctor = self.object
        save_audit(self.request, doctor, action='M')
        messages.success(self.request, f"Éxito al Modificar el doctor {doctor.nombre_completo}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al Modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

class DoctorDeleteView(LoginRequiredMixin,DeleteViewMixin,DeleteView):
    model = Doctor
    success_url = reverse_lazy('core:doctor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Doctor'
        context['description'] = f"¿Desea eliminar al doctor: {self.object.nombre_completo}?"
        context['back_url'] = self.success_url
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente al doctor {self.object.nombre_completo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)

class DoctorDetailView(LoginRequiredMixin,DetailView):
    model = Doctor

    def get(self, request, *args, **kwargs):
        doctor = self.get_object()
        data = {
            'id': doctor.id,
            'nombres': doctor.nombres,
            'apellidos': doctor.apellidos,
            'cedula': doctor.cedula,
            'foto': doctor.get_image(),
            'fecha_nacimiento': doctor.fecha_nacimiento,
            'edad': doctor.calcular_edad(doctor.fecha_nacimiento),
            'especialidad': doctor.especialidad,
            'direccion': doctor.direccion,
            'latitud': doctor.latitud,
            'longitud': doctor.longitud,
            'codigoUnicoDoctor': doctor.codigoUnicoDoctor,
            'telefonos': doctor.telefonos,
            'email': doctor.email,
            'horario_atencion': doctor.horario_atencion,
            'duracion_cita': doctor.duracion_cita,
            'curriculum': doctor.curriculum,
            'firmaDigital': doctor.firmaDigital,
            'imagen_receta': doctor.imagen_receta,
        }
        return JsonResponse(data)