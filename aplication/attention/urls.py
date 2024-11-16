from django.urls import path
from aplication.attention.views.medical_attention import AttentionCreateView, AttentionDetailView, AttentionListView, AttentionUpdateView
from aplication.attention.views.citaMedica import CitaMedicaCreateView, CitaMedicaListView, CitaMedicaUpdateView, CitaMedicaDeleteView, CitaMedicaDetailView

app_name='attention' # define un espacio de nombre para la aplicacion

urlpatterns = [
  # rutas de atenciones
  path('attention_list/',AttentionListView.as_view() ,name="attention_list"),
  path('attention_create/', AttentionCreateView.as_view(),name="attention_create"),
  path('attention_update/<int:pk>/', AttentionUpdateView.as_view(),name='attention_update'),
  path('attention_detail/<int:pk>/', AttentionDetailView.as_view(),name='attention_detail'),
  # path('patient_delete/<int:pk>/', PatientDeleteView.as_view(),name='patient_delete'),
  
  # Cita Medica
  path('cita_list/',CitaMedicaListView.as_view() ,name="citaMedica_list"),
  path('cita_create/', CitaMedicaCreateView.as_view(),name="citaMedica_create"),
  path('cita_update/<int:pk>/', CitaMedicaUpdateView.as_view(),name='citaMedica_update'),
  path('cita_detail/<int:pk>/', CitaMedicaDetailView.as_view(),name='citaMedica_detail'),
  path('cita_delete/<int:pk>/', CitaMedicaDeleteView.as_view(),name='citaMedica_delete'),
]
