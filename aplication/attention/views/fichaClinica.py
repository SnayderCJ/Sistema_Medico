from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View
from django.db.models import Q
from django.http import HttpResponse
from aplication.core.models import Paciente
from aplication.attention.models import Atencion, DetalleAtencion, Certificado
from doctor.mixins import ListViewMixin
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from io import BytesIO


class FichaClinicaListView(LoginRequiredMixin, ListViewMixin, ListView):
   template_name = "attention/fichaClinica/list.html"
   model = Paciente
   context_object_name = 'pacientes'
    
   def get_queryset(self):
      query = self.request.GET.get('q')
      if query:
         return Paciente.objects.filter(
               Q(nombres__icontains=query) |
               Q(apellidos__icontains=query) |
               Q(cedula__icontains=query)
         )
      return Paciente.objects.all()
   
class FichaClinicaDetailView(LoginRequiredMixin, DetailView):
    template_name = "attention/fichaClinica/detail.html"
    model = Paciente
    context_object_name = 'paciente'
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente = self.get_object()
      
        context.update({
            'atenciones': Atencion.objects.filter(paciente=paciente).order_by('-fecha_atencion'),
            'medicamentos': DetalleAtencion.objects.filter(atencion__paciente=paciente).select_related('medicamento'),
            'certificados': Certificado.objects.filter(paciente=paciente).order_by('-fecha_emision'),
            'edad': self.calcular_edad(paciente.fecha_nacimiento)
        })

        self._add_ultima_atencion_data(context, paciente)
        self._add_historial_diagnosticos(context)

        return context
     
    def calcular_edad(self, fecha_nacimiento):
        from datetime import date
        today = date.today()
        return today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    def _add_ultima_atencion_data(self, context, patient):
        ultima_atencion = Atencion.objects.filter(paciente=patient).order_by('-fecha_atencion').first()
        if ultima_atencion:
            context['ultima_atencion'] = ultima_atencion
            if ultima_atencion.peso and ultima_atencion.altura:
                imc = float(ultima_atencion.calcular_imc)
                context['imc'] = imc
                context['imc_clasificacion'] = self._get_imc_classification(imc)
                  
    def _get_imc_classification(self, imc):
        if imc < 18.5:
            return 'Bajo peso'
        elif 18.5 <= imc < 25:
            return 'Peso normal'
        elif 25 <= imc < 30:
            return 'Sobrepeso'
        return 'Obesidad'

    def _add_historial_diagnosticos(self, context):
        diagnosticos = set()
        for atencion in context['atenciones']:
            diagnosticos.update(atencion.diagnostico.all())
        context['historial_diagnosticos'] = list(diagnosticos)
      
      
class ImprimirHistorialClinico(View):
    def get(self, request, pk):
        paciente = Paciente.objects.get(pk=pk)
        atenciones = Atencion.objects.filter(paciente=paciente).order_by('-fecha_atencion')
        medicamentos = DetalleAtencion.objects.filter(atencion__paciente=paciente)
        certificados = Certificado.objects.filter(paciente=paciente)


        # Contexto para la plantilla HTML
        context = {
            'paciente': paciente,
            'atenciones': atenciones,
            'medicamentos': medicamentos,
            'certificados': certificados,
            'edad': FichaClinicaDetailView().calcular_edad(paciente.fecha_nacimiento)
        }

        # Renderizar el HTML
        html_string = render_to_string('attention/fichaClinica/fichaClinica.html', context)

        # Generar el PDF con WeasyPrint
        pdf_file = BytesIO()
        HTML(string=html_string).write_pdf(pdf_file)

        # Devolver el PDF como respuesta HTTP
        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="historial_clinico_{paciente.apellidos}_{paciente.nombres}.pdf"'
        )
        return response