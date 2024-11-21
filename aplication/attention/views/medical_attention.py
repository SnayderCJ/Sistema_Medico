from django.utils import timezone
from decimal import Decimal
import json
from django.urls import reverse_lazy
from django.db import transaction
from aplication.attention.forms.medical_attention import AttentionForm
from aplication.attention.models import Atencion, DetalleAtencion, ExamenSolicitado
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from aplication.core.models import Diagnostico, Medicamento
from doctor.mixins import CreateViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import custom_serializer, save_audit

class AttentionListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "attention/medical_attention/list.html"
    model = Atencion
    context_object_name = 'atenciones'
    # query = None
    # paginate_by = 2
    
    def get_queryset(self):
        # self.query = Q()
        q1 = self.request.GET.get('q') # ver
        sex= self.request.GET.get('sex')
        if q1 is not None: 
            self.query.add(Q(paciente__nombres__icontains=q1), Q.OR) 
            self.query.add(Q(paciente__apellidos__icontains=q1), Q.OR) 
            self.query.add(Q(paciente__cedula__icontains=q1), Q.OR) 
        if sex == "M" or sex=="F": self.query.add(Q(paciente__sexo__icontains=sex), Q.AND)   
        return self.model.objects.filter(self.query).order_by('-fecha_atencion')
    
class AttentionCreateView(LoginRequiredMixin,CreateViewMixin, CreateView):
    model = Atencion
    template_name = 'attention/medical_attention/form.html'
    form_class = AttentionForm
    success_url = reverse_lazy('attention:attention_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def post(self, request):
        # Convertir el cuerpo de la solicitud a un diccionario Python
        data = json.loads(request.body)
        medicamentos = data['medicamentos']  
        #Crear una instancia del formulario y poblarla con los datos JSON
        try:
            with transaction.atomic():
                # Crear la instancia del modelo Atencion
                atencion = Atencion.objects.create(
                    paciente_id=int(data['paciente']),
                    presion_arterial=data['presionArterial'],
                    pulso=int(data['pulso']),
                    temperatura=Decimal(data['temperatura']),
                    frecuencia_respiratoria=int(data['frecuenciaRespiratoria']),
                    saturacion_oxigeno=Decimal(data['saturacionOxigeno']),
                    peso=Decimal(data['peso']),
                    altura=Decimal(data['altura']),
                    motivo_consulta=data['motivoConsulta'],
                    sintomas=data['sintomas'],
                    tratamiento=data['tratamiento'],
                    examen_fisico=data['examenFisico'],
                    comentario_adicional=data['comentarioAdicional'],
                    fecha_atencion= timezone.now()
                )
                diagnostico_ids = data.get('diagnostico', [])
                diagnosticos = Diagnostico.objects.filter(id__in=diagnostico_ids)
                atencion.diagnostico.set(diagnosticos)
                
                examenes_ids = data.get('examenesEnviados', [])
                examenes = ExamenSolicitado.objects.filter(id__in=examenes_ids)
                atencion.examenes_enviados.set(examenes)
                
                atencion.save()
                
                # Ahora procesamos el arreglo de medicamentos
                for medicamento in medicamentos:
                    #Crear el detalle de atención para cada medicamento
                    DetalleAtencion.objects.create(
                        atencion=atencion,
                        medicamento_id=int(medicamento['codigo']),
                        cantidad=int(medicamento['cantidad']),
                        prescripcion=medicamento['prescripcion'],
                        # Si necesitas la duración del tratamiento, puedes agregarla aquí
                    )
                
                save_audit(request, atencion, "A")
                messages.success(self.request, f"Éxito al registrar la atención médica #{atencion.id}")
                return JsonResponse({"msg": "Éxito al registrar la atención médica."}, status=200)

        except Exception as ex:
            messages.error(self.request, "Érro al registrar la atención médica")
            return JsonResponse({"msg": str(ex)}, status=400)
        
      

class AttentionUpdateView(LoginRequiredMixin,UpdateViewMixin,UpdateView):
    model = Atencion
    template_name = 'attention/medical_attention/form.html'
    form_class = AttentionForm
    success_url = reverse_lazy('attention:attention_list')
    # permission_required = 'add_supplier' # en PermissionMixn se verfica si un grupo tiene el permiso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["medications"] = Medicamento.active_medication.values('id','nombre').order_by('nombre')
        detail_atencion = list(DetalleAtencion.objects.filter(atencion_id=self.object.id).values("medicamento_id","medicamento__nombre","cantidad","prescripcion"))
        detail_atencion = json.dumps(detail_atencion, default=custom_serializer)
        context['detail_atencion'] = detail_atencion 
        context['examenes'] = ExamenSolicitado.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        medicamentos = data['medicamentos']  
        try:
            atencion = Atencion.objects.get(id=self.kwargs.get('pk'))
            with transaction.atomic():
                atencion.paciente_id = int(data['paciente'])
                atencion.presion_arterial = data['presionArterial']
                atencion.pulso = int(data['pulso'])
                atencion.temperatura = Decimal(data['temperatura'])
                atencion.frecuencia_respiratoria = int(data['frecuenciaRespiratoria'])
                atencion.saturacion_oxigeno = Decimal(data['saturacionOxigeno'])
                atencion.peso = Decimal(data['peso'])
                atencion.altura = Decimal(data['altura'])
                atencion.motivo_consulta = data['motivoConsulta']
                atencion.sintomas = data['sintomas']
                atencion.tratamiento = data['tratamiento']
                atencion.examen_fisico = data['examenFisico']
                atencion.comentario_adicional = data['comentarioAdicional']
                
                diagnostico_ids = data.get('diagnostico', [])
                diagnosticos = Diagnostico.objects.filter(id__in=diagnostico_ids)
                atencion.diagnostico.set(diagnosticos)
                
                examenes_ids = data.get('examenesEnviados', [])
                examenes = ExamenSolicitado.objects.filter(id__in=examenes_ids)
                atencion.examenes_enviados.set(examenes)
                
                atencion.save()
                
                DetalleAtencion.objects.filter(atencion_id=atencion.id).delete()
                for medicamento in medicamentos:
                    DetalleAtencion.objects.create(
                        atencion=atencion,
                        medicamento_id=int(medicamento['codigo']),
                        cantidad=int(medicamento['cantidad']),
                        prescripcion=medicamento['prescripcion'],
                    )
                
                save_audit(request, atencion, "M")
                messages.success(self.request, f"Éxito al Actualizar la atención médica #{atencion.id}")
                return JsonResponse({"msg": "Éxito al Actualizar la atención médica."}, status=200)
        except Exception as ex:
            messages.error(self.request, "Érro al actualizar la atención médica")
            return JsonResponse({"msg": str(ex)}, status=400)
        
class AttentionDetailView(LoginRequiredMixin,DetailView):
    model = Atencion
    
    def get(self):
        atencion = self.get_object()
        detail_atencion =list(DetalleAtencion.objects.filter(atencion_id=atencion.id).values("medicamento_id","medicamento__nombre","cantidad","prescripcion"))
        detail_atencion=json.dumps(detail_atencion,default=custom_serializer)
        data = {
            'id': atencion.id,
            'nombres': atencion.paciente.nombre_completo,
            'foto': atencion.paciente.get_image(),
            'detalle_atencion': detail_atencion
        }
        return JsonResponse(data)