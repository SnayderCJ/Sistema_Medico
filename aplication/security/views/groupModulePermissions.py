from aplication.security.mixins.mixins import CreateViewMixin, DeleteViewMixin, ListViewMixin, PermissionMixin, UpdateViewMixin
from aplication.security.forms.group_module_permissions import GroupModulePermissionForm
from aplication.security.models import GroupModulePermission, Module, Group, Permission, User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q


# vista para el buscadador dinamico
class GroupModulePermissionSuggestionsView(ListView):
  def get(self, request, *args, **kwargs):
    term = request.GET.get('term', '')
    suggestions = GroupModulePermission.objects.filter(
      Q(group__name__icontains=term) | Q(module__name__icontains=term)
    ).values('module__name')[:10]
    suggestions_list = list(suggestions)
    return JsonResponse(suggestions_list, safe=False)


def get_group_permissions(self, group_id):
  all_modules = Module.objects.all()
  group_modules_permissions = GroupModulePermission.objects.filter(group_id=group_id).select_related('module')
  assigned_modules = {gmp.module.id: list(gmp.permissions.values('id', 'name')) for gmp in group_modules_permissions}

  permissions_data = []
  for module in all_modules:
    module_data = {
      'module_id': module.id,
      'module_name': module.name,
      'permissions': list(module.permissions.values('id', 'name')),
      'assigned_permissions': assigned_modules.get(module.id, [])
    }
    permissions_data.append(module_data)
  print(JsonResponse(permissions_data, safe=False))
  return JsonResponse(permissions_data, safe=False)


def get_module_permissions(request, module_id):
  try:
    module = Module.objects.get(id=module_id)
    permissions = list(module.permissions.values('id', 'name'))
    return JsonResponse(permissions, safe=False)
  except Module.DoesNotExist:
    return JsonResponse({'error': 'Módulo no encontrado'}, status=404)


class GroupModulePermissionListView(PermissionMixin, ListViewMixin, ListView):
  model = GroupModulePermission
  template_name = 'security/group_module_permission/list.html'
  context_object_name = 'grupomodulopermisos'
  permission_required = 'view_groupmodulepermission'

  def get_queryset(self):
    q = self.request.GET.get('q')
    query = Q()
    if q:
      query = Q(group__name__icontains=q) | Q(module__name__icontains=q)
    return GroupModulePermission.objects.filter(query).order_by('-id')

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['create_url'] = reverse_lazy('security:groupmodulepermission_create')
    context['title1'] = 'Grupos Módulos Permisos'
    context['title2'] = 'Consulta Grupos Módulos Permisos'
    return context


class GroupModulePermissionCreateView(PermissionMixin, CreateViewMixin, CreateView):
  model = GroupModulePermission
  form_class = GroupModulePermissionForm
  template_name = 'security/group_module_permission/form.html'
  success_url = reverse_lazy('security:groupmodulepermission_list')
  permission_required = 'add_groupmodulepermission'

  def get_context_data(self, **kwargs):
    context = super().get_context_data()
    context['title1'] = 'Grupo Módulo Permiso'
    context['title2'] = 'Asignar Permisos'
    context['back_url'] = self.success_url
    return context

  def form_valid(self, form):
    group = form.cleaned_data['group']
    GroupModulePermission.objects.filter(group=group).delete()
    modules_selected = self.request.POST.getlist('modules[]')

    for module_id in modules_selected:
      module = Module.objects.get(id=module_id)
      new_group_module_permission = GroupModulePermission.objects.create(
        group=group,
        module=module,
      )
      permissions_selected = self.request.POST.getlist(f'permissions_{module_id}[]')
      new_group_module_permission.permissions.set(permissions_selected)

    messages.success(self.request, "Grupo Módulos Permisos EXITOSO !!!.")
    print(modules_selected)
    print(redirect(self.success_url))
    return redirect(self.success_url)


# class GroupModulePermissionUpdateView(PermissionMixin, UpdateViewMixin, UpdateView):
#   model = GroupModulePermission
#   form_class = GroupModulePermissionForm
#   template_name = 'security/group_module_permission/form.html'
#   success_url = reverse_lazy('security:groupmodulepermission_list')
#   permission_required = 'change_groupmodulepermission'
#
#   def form_valid(self, form):
#     response = super().form_valid(form)
#     gmp = self.object
#     messages.success(self.request, f"Éxito al actualizar grupos modulos permisos {gmp.group.name}")
#     return response
#
#
# class GroupModulePermissionDeleteView(PermissionMixin, DeleteViewMixin, DeleteView):
#   model = GroupModulePermission
#   template_name = 'core/delete.html'
#   success_url = reverse_lazy('security:groupmodulepermission_list')
#   permission_required = 'delete_groupmodulepermission'
#
#   def __init__(self, *args, **kwargs):
#     super().__init__(args, kwargs)
#     self.object = None
#
#   def delete(self, request, *args, **kwargs):
#     self.object = self.get_object
#     self.object.delete()
#     messages.success(self.request, f"Grupos modulos permisos ' {self.object.module.name}'eliminado exitosamente.")
#     return super().delete(request, *args, **kwargs)
#
#   def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['description'] = f"¿Desea eliminar los permisos : {self.object.module.name}?"
#     return context
#
