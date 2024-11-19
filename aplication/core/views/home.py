from django.views.generic import TemplateView
from aplication.core.models import Paciente
from aplication.attention.models import CitaMedica
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
        context["can_cita"] = CitaMedica.cantidad_cita()
        
        return context