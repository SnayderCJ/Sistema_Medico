from django.views.generic import TemplateView
from aplication.core.models import Paciente
from aplication.attention.models import CitaMedica
from datetime import date
# import os
# from dotenv import load_dotenv

# Cargar las variables del archivo .env
# load_dotenv()

class HomeTemplateView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {"title": "SaludSync","title1": "Sistema Medico", "title2": "Sistema Medico"}
        # context['google_maps_api_key'] = os.getenv('KEY_GOOGLE_MAPS')
        context["can_paci"] = Paciente.cantidad_pacientes()
        context["ultimo_paciente"] = Paciente.objects.order_by('-id').first()
        # Contexto de cita
        context["can_cita"] = CitaMedica.cantidad_cita()
        context["proximas_citas"] = CitaMedica.objects.filter(fecha=date.today(), estado='P').order_by('hora_cita')
        context["ultima_cita_completada"] = CitaMedica.objects.filter(estado='R').order_by('-fecha', '-hora_cita').first()
        context["ultima_cita"] = CitaMedica.objects.order_by('-fecha', '-hora_cita').first()
        
        
        return context