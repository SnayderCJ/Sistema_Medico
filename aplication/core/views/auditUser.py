from django.views.generic import ListView
from aplication.core.models import AuditUser
from doctor.utils import save_audit
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import ListViewMixin

class AuditUserListView(LoginRequiredMixin,ListViewMixin,ListView):
    model = AuditUser
    template_name = 'core/audit/list.html'
    context_object_name = 'audit_users'
    paginate_by = 20  # Paginar la lista si es necesario

    def get_queryset(self):
        queryset = super().get_queryset()
        # Agregar filtros y ordenamiento si es necesario
        return queryset