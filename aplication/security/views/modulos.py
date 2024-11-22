from aplication.security.instance.menu_module import MenuModule
from aplication.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic import TemplateView
from aplication.security.models import Module, GroupModulePermission
from django.urls import reverse_lazy
from django.db.models import Q
from aplication.security.forms.modules import ModuleForm
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse


# vista para el buscadador dinamico
class ModuleSuggestionsView(ListView):
  def get(self, request, *args, **kwargs):
    term = request.GET.get('term', '')
    suggestions = Module.objects.filter(name__icontains=term).values('icon', 'name')[
                  :10]
    suggestions_list = list(suggestions)
    return JsonResponse(suggestions_list, safe=False)


class ModuloTemplateView(PermissionMixin, TemplateView):
  template_name = 'components/modulos.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["title1"] = "IC - Modulos"
    context["title2"] = "Modulos Disponibles"
    MenuModule(self.request).fill(context)
    print(context)
    return context


class ModuleListView(PermissionMixin, ListViewMixin, ListView):
  template_name = 'security/modulos/list.html'
  model = Module
  context_object_name = 'modules'
  permission_required = 'view_modules'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    for module in context['object_list']:
      module.can_be_deleted = not module.has_related_objects_Modules()
    return context

  def get_queryset(self):
    q1 = self.request.GET.get('q')
    if q1:
      query = Q(name__icontains=q1)
    else:
      query = Q(is_active=True)

    return self.model.objects.filter(query).order_by('id')


class ModuleCreateView(PermissionMixin, CreateViewMixin, CreateView):
  template_name = 'security/modulos/form.html'
  model = Module
  form_class = ModuleForm
  success_url = reverse_lazy('security:modules_list')
  permission_required = 'add_module'

  def form_valid(self, form):
    response = super().form_valid(form)
    module = self.object
    messages.success(self.request, f"Éxito al crear el módulo {module.name}.")
    return response


class ModuleUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
  model = Module
  template_name = 'security/modulos/form.html'
  form_class = ModuleForm
  success_url = reverse_lazy('security:modules_list')
  permission_required = 'change_module'

  def form_valid(self, form):
    response = super().form_valid(form)
    module = self.object
    messages.success(self.request, f"Éxito al actualizar el módulo {module.name}.")
    return response


class ModuleDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
  model = Module
  template_name = 'fragments/delete.html'
  success_url = reverse_lazy('security:modules_list')
  permission_required = 'delete_module'

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()

    # Verificar si existen relaciones con otros objetos
    if self.object.groupmodulepermission_set.exists():
      # Mostrar mensaje de error
      messages.error(request, "No se puede eliminar el módulo porque tiene relaciones con otros objetos.")
      return redirect(self.success_url)

    # Eliminación física del objeto Module
    success_url = self.get_success_url()
    self.object.delete()
    return redirect(success_url)
