from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from aplication.attention.models import Certificado
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
from aplication.attention.forms.certificado import CertificadoForm
# from reportlab.pdfgen import canvas
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.utils import save_audit


class GenerarCertificadoView(LoginRequiredMixin, CreateViewMixin, CreateView):
   
    model = Certificado
    form_class = CertificadoForm
    template_name = 'attention/generar_certificado.html'
    success_url = reverse_lazy('attention:certificado_list')  # O la URL que desees
    
class CertificadoListView(LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "attention/certificado/list.html"
    model = Certificado
    context_object_name = 'certificados'
    query = None
    paginate_by = 10
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')  # Ver
        status = self.request.GET.get('status')
        
        if q1 is not None: 
            self.query.add(Q(paciente__nombre__icontains=q1), Q.AND)
        
        if status == "activo":
            self.query.add(Q(activo=True), Q.AND)
        elif status == "inactivo":
            self.query.add(Q(activo=False), Q.AND)
        return self.model.objects.filter(self.query).order_by('-fecha_emision')
    
class CertificadoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Certificado
    template_name = 'attention/certificado/form.html'
    form_class = CertificadoForm  # Debes crear un formulario para Certificado
    success_url = reverse_lazy('attention:certificado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Certificado'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        certificado = self.object
        save_audit(self.request, certificado, action='A')
        messages.success(self.request, f"Éxito al crear el certificado de {certificado.paciente}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))

class CertificadoUpdateView(LoginRequiredMixin, UpdateViewMixin, UpdateView):
    model = Certificado
    template_name = 'attention/certificado/form.html'
    form_class = CertificadoForm  # Debes crear un formulario para Certificado
    success_url = reverse_lazy('attention:certificado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Certificado'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        certificado = self.object
        save_audit(self.request, certificado, action='M')
        messages.success(self.request, f"Éxito al modificar el certificado de {certificado.paciente}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al modificar el formulario. Corrige los errores.")
        return self.render_to_response(self.get_context_data(form=form))
    
class CertificadoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Certificado
    success_url = reverse_lazy('attention:certificado_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Certificado'
        context['description'] = f"¿Desea eliminar el certificado de {self.object.paciente}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar lógicamente el certificado de {self.object.paciente}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
    
class CertificadoDetailView(LoginRequiredMixin, DetailView):
    model = Certificado
    
    def get(self, request, *args, **kwargs):
        certificado = self.get_object()
        data = {
            'id': certificado.id,
            'paciente': certificado.paciente.nombre,
            'doctor': certificado.doctor.nombre,
            'fecha_emision': certificado.fecha_emision,
            'tipo_certificado': certificado.tipo_certificado,
            'observaciones': certificado.observaciones,
        }
        return JsonResponse(data)


