from django.urls import path
from aplication.attention.views.medical_attention import AttentionCreateView, AttentionDetailView, AttentionListView, AttentionUpdateView
from aplication.attention.views.horarioAtencion import HorarioAtencionCreateView, HorarioAtencionListView, HorarioAtencionUpdateView, HorarioAtencionDeleteView, HorarioAtencionDetailView
from aplication.attention.views.citaMedica import CitaMedicaCreateView, CitaMedicaListView, CitaMedicaUpdateView, CitaMedicaDeleteView, CitaMedicaDetailView
from aplication.attention.views.serviciosAdicionales import ServiciosAdicionalesCreateView, ServiciosAdicionalesListView, ServiciosAdicionalesUpdateView, ServiciosAdicionalesDeleteView, ServiciosAdicionalesDetailView
from aplication.attention.views.examenSolicitado import ExamenSolicitadoCreateView, ExamenSolicitadoListView, ExamenSolicitadoUpdateView, ExamenSolicitadoDeleteView, ExamenSolicitadoDetailView
from aplication.attention.views.certificado import CertificadoCreateView, CertificadoListView, CertificadoUpdateView, CertificadoDeleteView, CertificadoDetailView, CertificadoPDFView
from aplication.attention.views.fichaClinica import FichaClinicaListView, FichaClinicaDetailView, ImprimirHistorialClinico
from aplication.attention.views.costo_pago import PagoCreateView, PagoDetailView, PagoListView, PagoDeleteView, PagoComprobanteView, paypal_execute, verificar_pago_paciente, obtener_examenes_paciente, obtener_costos_completos_paciente

app_name = 'attention'

urlpatterns = [
  # rutas de atenciones
  path('attention_list/',AttentionListView.as_view() ,name="attention_list"),
  path('attention_create/', AttentionCreateView.as_view(),name="attention_create"),
  path('attention_update/<int:pk>/', AttentionUpdateView.as_view(),name='attention_update'),
  path('attention_detail/<int:pk>/', AttentionDetailView.as_view(),name='attention_detail'),
  # path('patient_delete/<int:pk>/', PatientDeleteView.as_view(),name='patient_delete'),
  
  # Horario de Atencion
  path('horario_list/',HorarioAtencionListView.as_view() ,name="horario_list"),
  path('horario_create/', HorarioAtencionCreateView.as_view(),name="horario_create"),
  path('horario_update/<int:pk>/', HorarioAtencionUpdateView.as_view(),name='horario_update'),
  path('horario_delete/<int:pk>/', HorarioAtencionDeleteView.as_view(),name='horario_delete'),
  path('horario_detail/<int:pk>/', HorarioAtencionDetailView.as_view(),name='horario_detail'),
  
  # Cita Medica
  path('cita_list/',CitaMedicaListView.as_view() ,name="citaMedica_list"),
  path('cita_create/', CitaMedicaCreateView.as_view(),name="citaMedica_create"),
  path('cita_update/<int:pk>/', CitaMedicaUpdateView.as_view(),name='citaMedica_update'),
  path('cita_detail/<int:pk>/', CitaMedicaDetailView.as_view(),name='citaMedica_detail'),
  path('cita_delete/<int:pk>/', CitaMedicaDeleteView.as_view(),name='citaMedica_delete'),
  
  # Servicios Adicionales
  path('servicio_list/',ServiciosAdicionalesListView.as_view() ,name="servicio_list"),
  path('servicio_create/', ServiciosAdicionalesCreateView.as_view(),name="servicio_create"),
  path('servicio_update/<int:pk>/', ServiciosAdicionalesUpdateView.as_view(),name='servicio_update'),
  path('servicio_delete/<int:pk>/', ServiciosAdicionalesDeleteView.as_view(),name='servicio_delete'),
  path('servicio_detail/<int:pk>/', ServiciosAdicionalesDetailView.as_view(),name='servicio_detail'),
  
  # Examen Solicitado
  path('examen_list/',ExamenSolicitadoListView.as_view() ,name="examen_list"),
  path('examen_create/', ExamenSolicitadoCreateView.as_view(),name="examen_create"),
  path('examen_update/<int:pk>/', ExamenSolicitadoUpdateView.as_view(),name='examen_update'),
  path('examen_delete/<int:pk>/', ExamenSolicitadoDeleteView.as_view(),name='examen_delete'),
  path('examen_detail/<int:pk>/', ExamenSolicitadoDetailView.as_view(),name='examen_detail'),
  
  # Certificado
  path('certificado_list/',CertificadoListView.as_view() ,name="certificado_list"),
  path('certificado_create/', CertificadoCreateView.as_view(),name="certificado_create"),
  path('certificado_update/<int:pk>/', CertificadoUpdateView.as_view(),name='certificado_update'),
  path('certificado_delete/<int:pk>/', CertificadoDeleteView.as_view(),name='certificado_delete'),
  path('certificado_detail/<int:pk>/', CertificadoDetailView.as_view(),name='certificado_detail'),
  path('certificado_pdf/<int:pk>/', CertificadoPDFView.as_view(), name='certificado_pdf'),
  
  # Ficha Clinica
  path('fichaClinica_list/', FichaClinicaListView.as_view(), name="fichaClinica_list"),
  path('ficha_clinica_detail/<int:pk>/', FichaClinicaDetailView.as_view(), name='fichaClinica_detail'),
  path('imprimirFichaClinica/<int:pk>/', ImprimirHistorialClinico.as_view(), name='imprimirFichaClinica'),
  
  # Pago
  path('pago_list/', PagoListView.as_view(), name="pago_list"),
  path('pago_create/', PagoCreateView.as_view(), name="pago_create"),
  path('pago_delete/<int:pk>/', PagoDeleteView.as_view(), name='pago_delete'),
  path('pago_detail/<int:pk>/', PagoDetailView.as_view(), name='pago_detail'),
  path('pago_comprobante/<int:pk>/', PagoComprobanteView.as_view(), name='pago_comprobante'),
  path('paypal_execute/', paypal_execute, name='paypal_execute'),
  path('verificar_pago_paciente/', verificar_pago_paciente, name='verificar_pago_paciente'),
  path('obtener_costos_completos_paciente/', obtener_costos_completos_paciente, name='obtener_costos_completos_paciente'),
  path('obtener_examenes_paciente/', obtener_examenes_paciente, name='obtener_examenes_paciente'),
  
]
