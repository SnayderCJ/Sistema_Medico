from django.views.generic import ListView
from aplication.core.models import AuditUser
from doctor.utils import save_audit
from django.contrib.auth.mixins import LoginRequiredMixin
from doctor.mixins import ListViewMixin

class AuditUserListView(LoginRequiredMixin,ListViewMixin,ListView):
    model = AuditUser
    template_name = "core/audit/list.html"
    context_object_name = "audits"
    paginate_by = 10

    def get_queryset(self):
        return AuditUser.objects.all().order_by('-fecha', '-hora')
