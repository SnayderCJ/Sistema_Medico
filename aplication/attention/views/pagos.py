from django.core.mail import EmailMessage
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from doctor.mixins import ListViewMixin, CreateViewMixin, UpdateViewMixin, DeleteViewMixin
from aplication.attention.models import Pago, CostosAtencion, ServiciosAdicionales, ExamenSolicitado
from aplication.attention.forms.pago import PagoForm
import paypalrestsdk
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

        metodo_pago = form.cleaned_data['metodo_pago']
        costo_atencion = form.cleaned_data['costo_atencion']
        servicios_adicionales = form.cleaned_data['servicios_adicionales']
        examenes_medicos = form.cleaned_data['examenes_medicos']

        total = Pago().calcular_total(costo_atencion, servicios_adicionales, examenes_medicos)

        if metodo_pago == 'PayPal':
            return self.process_paypal_payment(form, total)
        else:
            return self.process_cash_payment(form)

    def process_cash_payment(self, form):
        with transaction.atomic():
            pago = form.save(commit=False)
            pago.pagado = True
            pago.save()
            form.save_m2m()

            for examen in form.cleaned_data['examenes_medicos']:
                examen.pagado = True
                examen.save()

        messages.success(self.request, "El pago en efectivo se ha registrado correctamente.")
        return redirect(self.success_url)

    def process_paypal_payment(self, form, total):
        items = [{
            "name": "Costo Atención",
            "sku": "001",
            "price": str(form.cleaned_data['costo_atencion'].total),
            "currency": "USD",
            "quantity": 1
        }]

        for servicio in form.cleaned_data['servicios_adicionales']:
            items.append({
                "name": servicio.nombre_servicio,
                "sku": f"servicio_{servicio.id}",
                "price": str(servicio.costo_servicio),
                "currency": "USD",
                "quantity": 1
            })

        for examen in form.cleaned_data['examenes_medicos']:
            items.append({
                "name": examen.nombre_examen,
                "sku": f"examen_{examen.id}",
                "price": str(examen.precio_examen),
                "currency": "USD",
                "quantity": 1
            })

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
                "description": "Pago de atención médica"
            }]
        })

        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = str(link.href)
                    break

            self.request.session['servicios_adicionales'] = [s.id for s in form.cleaned_data['servicios_adicionales']]
            self.request.session['examenes_medicos'] = [e.id for e in form.cleaned_data['examenes_medicos']]

            return redirect(approval_url)
        else:
            messages.error(self.request, "Hubo un problema al procesar el pago con PayPal. Inténtalo de nuevo.")
            return redirect(self.success_url)


def paypal_execute(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        if payment.execute({"payer_id": payer_id}):
            costo_atencion_id = request.GET.get('costo_atencion_id')
            costo_atencion = get_object_or_404(CostosAtencion, pk=costo_atencion_id)

            pago = Pago.objects.create(
                paciente=costo_atencion.atencion.paciente,
                costo_atencion=costo_atencion,
                metodo_pago='PayPal',
                pagado=True
            )

            servicios_adicionales_ids = request.session.pop('servicios_adicionales', [])
            examenes_medicos_ids = request.session.pop('examenes_medicos', [])
            pago.servicios_adicionales.set(servicios_adicionales_ids)
            pago.examenes_medicos.set(examenes_medicos_ids)

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
        context['total_pagado'] = self.object.calcular_total_pagado()
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
    ha_pagado = Pago.objects.filter(paciente_id=paciente_id, pagado=True).exists()
    return JsonResponse({'ha_pagado': ha_pagado})


def obtener_examenes_paciente(request):
    paciente_id = request.GET.get('paciente_id')
    if not paciente_id:
        return JsonResponse({'error': 'El ID del paciente es obligatorio'}, status=400)

    examenes = ExamenSolicitado.objects.filter(atencion__paciente_id=paciente_id, activo=True, pagado=False)
    examenes_data = [{'id': examen.id, 'nombre': examen.nombre_examen, 'precio': str(examen.precio_examen)} for examen in examenes]
    return JsonResponse({'examenes': examenes_data})
