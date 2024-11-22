from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from django.views.generic import CreateView, ListView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from django.db import transaction
from weasyprint import HTML
from io import BytesIO
from django.conf import settings
from django.urls import reverse_lazy
import paypalrestsdk
from aplication.attention.models import (
    Pago,
    Atencion,
    CostosAtencion,
    ServiciosAdicionales,
    ExamenSolicitado,
    DetalleAtencion
)
from aplication.attention.forms.pago import PagoForm

# Configuración de PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # Cambiar a "live" en producción
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})

### VISTAS CLASE-BASED VIEWS ###

# Listar pagos
class PagoListView(LoginRequiredMixin, ListView):
    template_name = "attention/pago/list.html"
    model = Pago
    context_object_name = 'pagos'

# Crear un pago
class PagoCreateView(LoginRequiredMixin, CreateView):
    model = Pago
    template_name = 'attention/pago/form.html'
    form_class = PagoForm
    success_url = reverse_lazy('attention:pago_list')

    def obtener_costos_completos_paciente(self, paciente_id):
        costos_atencion = CostosAtencion.objects.filter(atencion__paciente_id=paciente_id, activo=True)
        total_costos_atencion = costos_atencion.aggregate(Sum('total'))['total__sum'] or 0

        servicios_adicionales = ServiciosAdicionales.objects.filter(
            costos_atenciones__costo_atencion__atencion__paciente_id=paciente_id
        )
        total_servicios_adicionales = servicios_adicionales.aggregate(Sum('costo_servicio'))['costo_servicio__sum'] or 0

        examenes = ExamenSolicitado.objects.filter(paciente_id=paciente_id)
        total_examenes = examenes.aggregate(Sum('costo'))['costo__sum'] or 0

        return total_costos_atencion + total_servicios_adicionales + total_examenes

    def validar_costo_atencion(self, atencion):
        """
        Verifica si ya existe un registro de CostosAtencion para una atención dada.
        Si no existe, lo crea.
        """
        if not CostosAtencion.objects.filter(atencion=atencion).exists():
            CostosAtencion.objects.create(
                atencion=atencion,
                costo_consulta=10.00,  # Valor por defecto
                descripcion="Consulta médica general",
                activo=True
            )

    def form_valid(self, form):
        paciente = form.cleaned_data['paciente']
        atencion = paciente.doctores_atencion.first()  # Asume que el paciente tiene una atención asociada.

        if not atencion:
            messages.error(self.request, "El paciente no tiene atenciones asociadas.")
            return redirect(self.success_url)

        self.validar_costo_atencion(atencion)  # Valida o crea el costo de atención.

        total_costos = self.obtener_costos_completos_paciente(paciente.id)

        if total_costos == 0:
            messages.warning(self.request, "No hay costos pendientes para este paciente.")
            return redirect(self.success_url)

        metodo_pago = form.cleaned_data['metodo_pago']
        if metodo_pago == 'PayPal':
            return self.process_paypal_payment(form, total_costos)
        return self.process_cash_payment(form)

    def process_cash_payment(self, form):
        try:
            with transaction.atomic():
                form.save()
            messages.success(self.request, "El pago en efectivo se ha registrado correctamente.")
        except Exception as e:
            messages.error(self.request, f"Error al registrar el pago: {e}")
        return redirect(self.success_url)

    def process_paypal_payment(self, form, total):
        items = [{
            "name": "Pago Médico",
            "sku": "001",
            "price": str(total),
            "currency": "USD",
            "quantity": 1
        }]

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": self.request.build_absolute_uri(reverse_lazy('attention:paypal_execute')),
                "cancel_url": self.request.build_absolute_uri(reverse_lazy('attention:pago_list'))
            },
            "transactions": [{
                "item_list": {"items": items},
                "amount": {"total": str(total), "currency": "USD"},
                "description": "Pago de servicios médicos"
            }]
        })

        if payment.create():
            return redirect(next(link.href for link in payment.links if link.rel == "approval_url"))
        messages.error(self.request, "Hubo un problema al procesar el pago con PayPal.")
        return redirect(self.success_url)


# Detalle de un pago
class PagoDetailView(LoginRequiredMixin, DetailView):
    model = Pago
    template_name = 'attention/pago/detail.html'
    context_object_name = 'pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pagado'] = self.object.monto
        return context

# Comprobante de pago (PDF)
class PagoComprobanteView(View):
    def get(self, request, *args, **kwargs):
        pago = get_object_or_404(Pago, pk=self.kwargs['pk'])
        context = {
            'pago': pago,
            'total_pagado': pago.monto,
        }
        html = get_template('attention/pago/comprobante.html').render(context)
        pdf = BytesIO()
        HTML(string=html).write_pdf(pdf)

        response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="comprobante_pago_{pago.pk}.pdf"'

        return response

# Eliminar un pago
class PagoDeleteView(LoginRequiredMixin, DeleteView):
    model = Pago
    template_name = 'attention/pago/confirm_delete.html'
    success_url = reverse_lazy('attention:pago_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, "El pago ha sido eliminado correctamente.")
        return redirect(self.success_url)

### FUNCIONES (API JSON RESPONSES) ###

# Procesar el pago con PayPal
def paypal_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            messages.success(request, "El pago con PayPal se ha procesado correctamente.")
            return redirect('attention:pago_list')
        raise Exception(payment.error)
    except Exception as e:
        messages.error(request, f"Error en PayPal: {e}")
        return redirect('attention:pago_list')

# Verificar si un paciente tiene pagos
def verificar_pago_paciente(request):
    paciente_id = request.GET.get('paciente_id')

    if not paciente_id:
        return JsonResponse({'error': 'El ID del paciente es obligatorio'}, status=400)

    atencion = Atencion.objects.filter(paciente_id=paciente_id).first()
    if not atencion:
        return JsonResponse({'error': 'No se encontró ninguna atención asociada al paciente.'}, status=400)

    # Verifica o crea costos de atención
    if not CostosAtencion.objects.filter(atencion=atencion).exists():
        CostosAtencion.objects.create(
            atencion=atencion,
            costo_consulta=100.00,
            descripcion="Consulta médica general",
            activo=True
        )

    ha_pagado = Pago.objects.filter(paciente_id=paciente_id, pagado=True).exists()
    return JsonResponse({'ha_pagado': ha_pagado})


# Obtener los exámenes pendientes de un paciente
def obtener_examenes_paciente(request):
    paciente_id = request.GET.get('paciente_id')
    examenes = ExamenSolicitado.objects.filter(atencion__paciente_id=paciente_id, estado='Pendiente')
    examenes_data = [{'id': ex.id, 'nombre': ex.nombre_examen, 'precio': str(ex.costo)} for ex in examenes]
    return JsonResponse({'examenes': examenes_data})

# Obtener los costos completos de un paciente
def obtener_costos_completos_paciente(request):
    paciente_id = request.GET.get('paciente_id')
    if not paciente_id:
        return JsonResponse({'error': 'El ID del paciente es obligatorio'}, status=400)
    
    # Verificar que el paciente tiene al menos una atención
    atencion = Atencion.objects.filter(paciente_id=paciente_id).first()
    if not atencion:
        return JsonResponse({'error': 'No se encontró ninguna atención asociada al paciente.'}, status=400)

    # Calcular costos de atención
    costos_atencion = CostosAtencion.objects.filter(atencion__paciente_id=paciente_id, activo=True)
    print(f"Costos de atención encontrados: {costos_atencion}")
    total_costos_atencion = costos_atencion.aggregate(Sum('total'))['total__sum'] or 0
    print(f"Total de costos de atención: {total_costos_atencion}")

    # Calcular costos de servicios adicionales
    servicios_adicionales = ServiciosAdicionales.objects.filter(
        costo_atencion__atencion__paciente_id=paciente_id
    )
    print(f"Servicios adicionales encontrados: {servicios_adicionales}")
    total_servicios_adicionales = servicios_adicionales.aggregate(Sum('costo_servicio'))['costo_servicio__sum'] or 0
    print(f"Total de servicios adicionales: {total_servicios_adicionales}")

    # Calcular costos de exámenes
    examenes = ExamenSolicitado.objects.filter(atencion__paciente_id=paciente_id)
    print(f"Exámenes encontrados: {examenes}")
    total_examenes = examenes.aggregate(Sum('costo'))['costo__sum'] or 0
    print(f"Total de exámenes: {total_examenes}")

    # Calcular costos de medicinas
    medicinas = DetalleAtencion.objects.filter(atencion__paciente_id=paciente_id)
    print(f"Medicinas encontradas: {medicinas}")
    total_medicinas = sum(
        detalle.medicamento.precio * detalle.cantidad for detalle in medicinas
    )
    print(f"Total de medicinas: {total_medicinas}")

    # Total general
    total_general = total_costos_atencion + total_servicios_adicionales + total_examenes + total_medicinas
    print(f"Total general: {total_general}")

    # Devolver la respuesta JSON con los costos
    return JsonResponse({
        'costos_atencion': str(total_costos_atencion),
        'servicios_adicionales': str(total_servicios_adicionales),
        'examenes': str(total_examenes),
        'medicinas': str(total_medicinas),
        'total_general': str(total_general)
    })




