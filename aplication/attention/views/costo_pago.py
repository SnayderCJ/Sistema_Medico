import paypalrestsdk
from io import BytesIO
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from doctor.mixins import ListViewMixin, CreateViewMixin, DeleteViewMixin
from aplication.attention.models import (
    Pago, 
    CostosAtencion, 
    ServiciosAdicionales, 
    ExamenSolicitado,
    CostoAtencionDetalle, 
)
from aplication.attention.forms.pago import PagoForm
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from weasyprint import HTML
from django.conf import settings
from django.db import transaction

# Configurar PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Cambia a "live" para producción
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})

class PagoListView(LoginRequiredMixin, ListViewMixin, ListView):
    template_name = "attention/pago/list.html"
    model = Pago
    context_object_name = 'pagos'

class PagoCreateView(LoginRequiredMixin, CreateViewMixin, CreateView):
    model = Pago
    template_name = 'attention/pago/form.html'
    form_class = PagoForm
    success_url = reverse_lazy('attention:pago_list')

    def form_valid(self, form):
        paciente = form.cleaned_data['paciente']
        costo_atencion = form.cleaned_data['costo_atencion']

        if Pago.objects.filter(paciente=paciente, costo_atencion=costo_atencion, pagado=True).exists():
            messages.warning(self.request, "El paciente ya tiene un pago registrado para esta atención.")
            return redirect(self.success_url)

        with transaction.atomic():
            pago = form.save(commit=False) 
            pago.monto = pago.costo_atencion.total  # Obtener el total de CostosAtencion
            pago.save()

            # Guardar servicios adicionales en CostoAtencionDetalle
            for servicio in form.cleaned_data['servicios_adicionales']:
                CostoAtencionDetalle.objects.create(
                    costo_atencion=pago.costo_atencion,
                    servicios_adicionales=servicio,
                )

            # Si necesitas guardar los exámenes en CostoAtencionDetalle:
            for examen in form.cleaned_data['examenes_medicos']:
                CostoAtencionDetalle.objects.create(
                    costo_atencion=pago.costo_atencion,
                    examen_solicitado=examen,  # Asumiendo que agregaste un campo 'examen_solicitado' en CostoAtencionDetalle
                )

            messages.success(self.request, "El pago se ha registrado correctamente.")
        return redirect(self.success_url)
    
def paypal_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            costo_atencion_id = request.GET.get('costo_atencion_id')
            costo_atencion = get_object_or_404(CostosAtencion, pk=costo_atencion_id)

            with transaction.atomic():
                pago = Pago.objects.create(
                    paciente=costo_atencion.atencion.paciente,
                    costo_atencion=costo_atencion,
                    metodo_pago='PayPal',
                    pagado=True
                )

                servicios_adicionales_ids = request.session.pop('servicios_adicionales', [])
                examenes_medicos_ids = request.session.pop('examenes_medicos', [])
                servicios_adicionales = ServiciosAdicionales.objects.filter(pk__in=servicios_adicionales_ids)
                examenes_medicos = ExamenSolicitado.objects.filter(pk__in=examenes_medicos_ids)
                pago.servicios_adicionales.set(servicios_adicionales)
                pago.examenes_medicos.set(examenes_medicos)

                costo_atencion.pagado = True
                costo_atencion.save()

            messages.success(request, "El pago con PayPal se ha procesado correctamente.")
            return redirect('attention:pago_list')
        else:
            raise Exception(payment.error)
    except Exception as e:
        print(f"Error en PayPal: {e}")
        messages.error(request, "Hubo un problema al confirmar el pago.")
        return redirect('attention:pago_list')

class PagoDetailView(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'attention/pago/detail.html'
    context_object_name = 'pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pagado'] = self.object.costo_atencion.total 
        return context

class PagoDeleteView(LoginRequiredMixin, DeleteViewMixin, DeleteView):
    model = Pago
    template_name = 'attention/pago/confirm_delete.html'
    success_url = reverse_lazy('attention:pago_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "El pago ha sido eliminado correctamente.")
        return redirect(self.success_url)

class PagoComprobanteView(View):
    def get(self, request, *args, **kwargs):
        pago = get_object_or_404(Pago, pk=self.kwargs['pk'])
        context = {
            'pago': pago,
            'total_pagado': pago.calcular_total_pagado(),
            'servicios_adicionales': pago.servicios_adicionales.all(),
            'examenes_medicos': pago.examenes_medicos.all(),
        }
        html = get_template('attention/pago/comprobante.html').render(context)
        pdf = BytesIO()
        HTML(string=html).write_pdf(pdf)

        response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="comprobante_pago_{pago.pk}.pdf"'

        return response

def verificar_pago_paciente(request):
    paciente_id = request.GET.get('paciente_id')
    # Ajusta la lógica según tu nuevo modelo
    ha_pagado = Pago.objects.filter(paciente_id=paciente_id, pagado=True).exists()  
    return JsonResponse({'ha_pagado': ha_pagado})

def obtener_examenes_paciente(request):
    paciente_id = request.GET.get('paciente_id')
    if not paciente_id:
        return JsonResponse({'error': 'El ID del paciente es obligatorio'}, status=400)
    # Ajusta la lógica según tu nuevo modelo, 
    # considerando la relación entre ExamenSolicitado y Atencion
    examenes = ExamenSolicitado.objects.filter(atencion__paciente_id=paciente_id, estado='Pendiente') 
    examenes_data = [{'id': examen.id, 'nombre': examen.nombre_examen, 'precio': str(examen.costo)} for examen in examenes]
    return JsonResponse({'examenes': examenes_data})