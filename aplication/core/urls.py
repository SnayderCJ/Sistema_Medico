from django.urls import path
from aplication.core.views.home import HomeTemplateView
from aplication.core.views.patient import PatientCreateView, PatientDeleteView, PatientDetailView, PatientListView, PatientUpdateView
from aplication.core.views.tipoSangre import TipoSangreListView, TipoSangreCreateView, TipoSangreUpdateView, TipoSangreDeleteView, TipoSangreDetailView
from aplication.core.views.especialidad import EspecialidadListView, EspecialidadCreateView, EspecialidadUpdateView, EspecialidadDeleteView, EspecialidadDetailView
from aplication.core.views.doctor import DoctorListView, DoctorCreateView, DoctorUpdateView, DoctorDeleteView, DoctorDetailView
from aplication.core.views.cargo import CargoListView, CargoCreateView, CargoUpdateView, CargoDeleteView, CargoDetailView
from aplication.core.views.empleado import EmpleadoListView, EmpleadoCreateView, EmpleadoUpdateView, EmpleadoDeleteView, EmpleadoDetailView
from aplication.core.views.tipoMedicamento import TipoMedicamentoListView, TipoMedicamentoCreateView, TipoMedicamentoUpdateView, TipoMedicamentoDeleteView, TipoMedicamentoDetailView
from aplication.core.views.marcaMedicamento import MarcaMedicamentoListView, MarcaMedicamentoCreateView, MarcaMedicamentoUpdateView, MarcaMedicamentoDeleteView
from aplication.core.views.medicamento import MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView, MedicamentoDetailView 
from aplication.core.views.diagnostico import DiagnosticoListView, DiagnosticoCreateView, DiagnosticoUpdateView, DiagnosticoDeleteView, DiagnosticoDetailView
from aplication.core.views.auditUser import AuditUserListView
 
 
 
app_name='core' # define un espacio de nombre para la aplicacion
urlpatterns = [
  # ruta principal
  path('', HomeTemplateView.as_view(),name='home'),
  
  
  
  path('patient_list/',PatientListView.as_view() ,name="patient_list"),
  path('patient_create/', PatientCreateView.as_view(),name="patient_create"),
  path('patient_update/<int:pk>/', PatientUpdateView.as_view(),name='patient_update'),
  path('patient_delete/<int:pk>/', PatientDeleteView.as_view(),name='patient_delete'),
  path('patient_detail/<int:pk>/', PatientDetailView.as_view(),name='patient_detail'),
  
  # Tipo de Sangre
  path('tipoSangre_list/', TipoSangreListView.as_view(), name="tipoSangre_list"),
  path('tipoSangre_create/', TipoSangreCreateView.as_view(), name="tipoSangre_create"),
  path('tipoSangre_update/<int:pk>/', TipoSangreUpdateView.as_view(), name="tipoSangre_update"),
  path('tipoSangre_delete/<int:pk>/', TipoSangreDeleteView.as_view(), name="tipoSangre_delete"),
  path('tipoSangre_detail/<int:pk>/', TipoSangreDetailView.as_view(), name="tipoSangre_detail"),
  
  # Especialidad
  path('especialidad_list/', EspecialidadListView.as_view(), name="especialidad_list"),
  path('especialidad_create/', EspecialidadCreateView.as_view(), name="especialidad_create"),
  path('especialidad_update/<int:pk>/', EspecialidadUpdateView.as_view(), name="especialidad_update"),
  path('especialidad_delete/<int:pk>/', EspecialidadDeleteView.as_view(), name="especialidad_delete"),
  path('especialidad_detail/<int:pk>/', EspecialidadDetailView.as_view(), name="especialidad_detail"),
  
  # Doctor
  path('doctor_list/', DoctorListView.as_view(), name="doctor_list"),
  path('doctor_create/', DoctorCreateView.as_view(), name="doctor_create"),
  path('doctor_update/<int:pk>/', DoctorUpdateView.as_view(), name="doctor_update"),
  path('doctor_delete/<int:pk>/', DoctorDeleteView.as_view(), name="doctor_delete"),
  path('doctor_detail/<int:pk>/', DoctorDetailView.as_view(), name="doctor_detail"),
  
  # Cargo 
  path('cargo_list/', CargoListView.as_view(), name="cargo_list"),
  path('cargo_create/', CargoCreateView.as_view(), name="cargo_create"),
  path('cargo_update/<int:pk>/', CargoUpdateView.as_view(), name="cargo_update"),
  path('cargo_delete/<int:pk>/', CargoDeleteView.as_view(), name="cargo_delete"),
  path('cargo_detail/<int:pk>/', CargoDetailView.as_view(), name="cargo_detail"),
  
  # Empleado 
  path('empleado_list/', EmpleadoListView.as_view(), name="empleado_list"),
  path('empleado_create/', EmpleadoCreateView.as_view(), name="empleado_create"),
  path('empleado_update/<int:pk>/', EmpleadoUpdateView.as_view(), name="empleado_update"),
  path('empleado_delete/<int:pk>/', EmpleadoDeleteView.as_view(), name="empleado_delete"),
  path('empleado_detail/<int:pk>/', EmpleadoDetailView.as_view(), name="empleado_detail"),
  
  # Tipo de Medicamento
  path('tipoMedicamento_list/', TipoMedicamentoListView.as_view(), name="tipoMedicamento_list"),
  path('tipoMedicamento_create/', TipoMedicamentoCreateView.as_view(), name="tipoMedicamento_create"),
  path('tipoMedicamento_update/<int:pk>/', TipoMedicamentoUpdateView.as_view(), name="tipoMedicamento_update"),
  path('tipoMedicamento_delete/<int:pk>/', TipoMedicamentoDeleteView.as_view(), name="tipoMedicamento_delete"),
  path('tipoMedicamento_detail/<int:pk>/', TipoMedicamentoDetailView.as_view(), name="tipoMedicamento_detail"),
  
  # Marca de Medicamento
  path('marcaMedicamento_list/', MarcaMedicamentoListView.as_view(), name="marcaMedicamento_list"),
  path('marcaMedicamento_create/', MarcaMedicamentoCreateView.as_view(), name="marcaMedicamento_create"),
  path('marcaMedicamento_update/<int:pk>/', MarcaMedicamentoUpdateView.as_view(), name="marcaMedicamento_update"),
  path('marcaMedicamento_delete/<int:pk>/', MarcaMedicamentoDeleteView.as_view(), name="marcaMedicamento_delete"),
  
  # Medicamento 
  path('medicamento_list/', MedicamentoListView.as_view(), name="medicamento_list"),
  path('medicamento_create/', MedicamentoCreateView.as_view(), name="medicamento_create"),
  path('medicamento_update/<int:pk>/', MedicamentoUpdateView.as_view(), name="medicamento_update"),
  path('medicamento_delete/<int:pk>/', MedicamentoDeleteView.as_view(), name="medicamento_delete"),
  path('medicamento_detail/<int:pk>/', MedicamentoDetailView.as_view(), name="medicamento_detail"),
  
  # Diagnostico
  path('diagnostico_list/', DiagnosticoListView.as_view(), name="diagnostico_list"),
  path('diagnostico_create/', DiagnosticoCreateView.as_view(), name="diagnostico_create"),
  path('diagnostico_update/<int:pk>/', DiagnosticoUpdateView.as_view(), name="diagnostico_update"),
  path('diagnostico_delete/<int:pk>/', DiagnosticoDeleteView.as_view(), name="diagnostico_delete"),
  path('diagnostico_detail/<int:pk>/', DiagnosticoDetailView.as_view(), name="diagnostico_detail"),
  
  # Auditoria
  path('auditoria/', AuditUserListView.as_view(), name='audit-list'),
]