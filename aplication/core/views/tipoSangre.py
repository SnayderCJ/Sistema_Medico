from django.urls import reverse_lazy
from aplication.core.forms.tipoSangre import TipoSangreForm
from aplication.core.models import TipoSangre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from doctor.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, UpdateViewMixin
from doctor.utils import save_audit

class TipoSangreListView(LoginRequiredMixin,ListViewMixin,ListView):
    template_name = "core/tipoSangre/list.html"
    model = TipoSangre
    context_object_name = 'Tipos_de_Sangre'
    query = None
    paginate_by = 2
    
    def get_queryset(self):
        self.query = Q()
        q1 = self.request.GET.get('q')  # Filtro de tipo de sangre
        q2 = self.request.GET.get('rh')  # Filtro de positivo o negativo
        
        if q1 is not None:
            self.query.add(Q(tipo__icontains=q1), Q.OR)

        if q2 is not None:
            if q2.lower() == 'positivo':
                self.query.add(Q(tipo__icontains='+'), Q.AND)
            elif q2.lower() == 'negativo':
                self.query.add(Q(tipo__icontains='-'), Q.AND)
        
        return self.model.objects.filter(self.query).order_by('tipo')
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = "Medical"
    #     context['title1'] = "Consulta de Tipo de Sangre"
    #     return context
    
    
class TipoSangreCreateView(LoginRequiredMixin,CreateViewMixin, CreateView):
    model = TipoSangre
    template_name = 'core/tipoSangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipoSangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Grabar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        save_audit(self.request, tipo_sangre, action='A')
        messages.success(self.request, f"Éxito al crear el tipo de sangre {tipo_sangre.tipo}.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
        

class TipoSangreUpdateView(LoginRequiredMixin,UpdateViewMixin,UpdateView):
    model = TipoSangre
    template_name = 'core/tipoSangre/form.html'
    form_class = TipoSangreForm
    success_url = reverse_lazy('core:tipoSangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Actualizar Tipo de Sangre'
        context['back_url'] = self.success_url
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        tipo_sangre = self.object
        save_audit(self.request, tipo_sangre, action='M')
        messages.success(self.request, f"Éxito al modificar el tipo de sangre {tipo_sangre.tipo}.")
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, "Error al enviar el formulario. Corrige los errores.")
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
class TipoSangreDeleteView(LoginRequiredMixin,DeleteViewMixin,DeleteView):
    model = TipoSangre
    success_url = reverse_lazy('core:tipoSangre_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['grabar'] = 'Eliminar Tipo de Sangre'
        context['description'] = f"¿Desea eliminar el tipo de sangre: {self.object.tipo}?"
        context['back_url'] = self.success_url
        return context
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_message = f"Éxito al eliminar el tipo de sangre {self.object.tipo}."
        messages.success(self.request, success_message)
        return super().delete(request, *args, **kwargs)
    
class TipoSangreDetailView(LoginRequiredMixin,DetailView):
    model = TipoSangre
    
    def get(self, request, *args, **kwargs):
        tipo_sangre = self.get_object()
        data = {
            'id': tipo_sangre.id,
            'tipo': tipo_sangre.tipo,
            'descripcion': tipo_sangre.descripcion,
            # Añade más campos según tu modelo
        }
        return JsonResponse(data)
