from django.urls import reverse_lazy
from aplication.attention.forms.citaMedica import CitaMedicaForm
from aplication.attention.models import CitaMedica
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.utils import save_audit
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

class CitaMedicaListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "attention/citaMedica/list.html"
    model = CitaMedica
    context_object_name = 'citas'
    query = None
    paginate_by = 10
    
    def get_queryset(self):
        query = Q()
        
        # Obtén los parámetros de búsqueda y filtro
        q = self.request.GET.get('q')
        estado = self.request.GET.get('estado')

        # Filtrar por nombre completo del paciente si 'q' está presente
        if q:
            query &= (Q(paciente__nombres__icontains=q) | Q(paciente__apellidos__icontains=q))

        # Filtrar por estado si 'estado' está presente
        if estado:
            query &= Q(estado=estado)
        
        return CitaMedica.objects.filter(query).order_by('fecha')
    
class CitaMedicaCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = CitaMedica
    template_name = 'attention/citaMedica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('attention:citaMedica_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar cita medica'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        # print("entro al form_valid")
        response = super().form_valid(form)
        citamedica = self.object
        
        # Envío de correo al paciente con formato mejorado
        subject = "🏥 Confirmación de tu Cita Médica"
        message = f"""
        ¡Hola {citamedica.paciente.nombres}!

        Tu cita médica ha sido programada exitosamente. A continuación, los detalles:

        📅 Fecha: {citamedica.fecha.strftime('%d/%m/%Y')}
        ⏰ Hora: {citamedica.hora_cita.strftime('%H:%M')}
        📋 Estado: {citamedica.estado}

        Recordatorios importantes:
        • Por favor, llegue 10 minutos antes de su cita
        • Traiga su documento de identidad
        • Si necesita cancelar, háganoslo saber con 24 horas de anticipación

        ¡Gracias por confiar en nuestros servicios médicos!

        Atentamente,
        El equipo médico
        ------------------------------------------
        Este es un correo automático, por favor no responder.
        """
        recipient_email = citamedica.paciente.email
        send_mail(
            subject,
            message,
            from_email=None,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        save_audit(self.request, citamedica, action='A')
        messages.success(self.request, f"Éxito al crear la cita medica del paciente: {citamedica.paciente}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class CitaMedicaUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model =CitaMedica
    template_name = 'attention/citaMedica/form.html'
    form_class = CitaMedicaForm
    success_url = reverse_lazy('attention:citaMedica_list')
    # permission_required = 'change_patient'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar cita medica'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        citamedica = self.object
        
        # Enviar correo electrónico de modificación de cita
        subject = "🏥 Tu Cita Médica ha sido Modificada"
        message = f"""
        ¡Hola {citamedica.paciente.nombres}!

        Te informamos que tu cita médica ha sido modificada. Los nuevos detalles son:

        📅 Fecha: {citamedica.fecha.strftime('%d/%m/%Y')}
        ⏰ Hora: {citamedica.hora_cita.strftime('%H:%M')}
        📋 Estado: {citamedica.get_estado_display()}

        Si tienes alguna pregunta, no dudes en contactarnos.

        Atentamente,
        El equipo médico
        ------------------------------------------
        Este es un correo automático, por favor no responder.
        """
        recipient_email = citamedica.paciente.email
        send_mail(
            subject,
            message,
            from_email=None,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        save_audit(self.request, citamedica, action='M')
        messages.success(self.request, f"Éxito al Modificar la cita medica del paciente : {citamedica.paciente}.")
        print("mande mensaje")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al Modificar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class CitaMedicaDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = CitaMedica
    # template_name = 'core/patient/form.html'
    success_url = reverse_lazy('attention:citaMedica_list')
    # permission_required = 'delete_supplier'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar cita medica'
        context['description'] = f"¿Desea Eliminar la cita medica: {self.object.name}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        citamedica = self.object
        
        # Enviar correo electrónico de cancelación de cita
        subject = "🏥 Tu Cita Médica ha sido Cancelada"
        message = f"""
        ¡Hola {citamedica.paciente.nombres}!

        Lamentamos informarte que tu cita médica ha sido cancelada. 

        Si deseas reprogramar tu cita, por favor contáctanos.

        Atentamente,
        El equipo médico
        ------------------------------------------
        Este es un correo automático, por favor no responder.
        """
        recipient_email = citamedica.paciente.email
        send_mail(
            subject,
            message,
            from_email=None,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        
        success_message = f"Éxito al eliminar lógicamente la cita medica {self.object.name}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
    
    
class CitaMedicaDetailView(LoginRequiredMixin,DetailView):
    model = CitaMedica
    
    def get(self, request, *args, **kwargs):
        citamedica = self.get_object()
        data = {
            'id': citamedica.id,
            'fecha': citamedica.fecha,
            'hora_cita': citamedica.hora_cita,
            'estado': citamedica.estado,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)
    
def enviar_notificacion_cita(cita, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        [cita.paciente.email],
        fail_silently=False,
    )

def enviar_recordatorios():
    hoy = timezone.now().date()  # Obtener la fecha de hoy

    citas_proximamente = CitaMedica.objects.filter(
        fecha__gte=hoy,  # Filtrar citas con fecha mayor o igual a hoy
        estado='P'       # 'P' para Programada
    )
    for cita in citas_proximamente:
        dias_hasta_cita = (cita.fecha - hoy).days  # Calcular los días hasta la cita

        if dias_hasta_cita == 0:
            asunto = 'Recordatorio de cita médica (hoy)'
            mensaje = f'Estimado(a) {cita.paciente.nombre_completo},\n\nLe recordamos que tiene una cita médica con el Dr. {cita.doctor.nombre_completo} hoy a las {cita.hora_cita}.\n\nAtentamente,\nClínica SaludSync'
        else:
            asunto = f'Recordatorio de cita médica (en {dias_hasta_cita} días)'
            mensaje = f'Estimado(a) {cita.paciente.nombre_completo},\n\nLe recordamos que tiene una cita médica con el Dr. {cita.doctor.nombre_completo} el {cita.fecha} a las {cita.hora_cita}.\n\nAtentamente,\nClínica SaludSync'

        enviar_notificacion_cita(cita, asunto, mensaje)