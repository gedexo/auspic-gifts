from django_tables2 import columns
from django_tables2 import Table

from .models import User

class BaseTable(Table):
    pk = columns.Column(visible=False)
    created = columns.DateTimeColumn(verbose_name="Created At", format="d/m/Y g:i A")
    action = columns.TemplateColumn(template_name="app/partials/table_actions.html", orderable=False)

    class Meta:
        attrs = {"class": "table  table-vcenter text-nowrap table-bordered border-bottom table-striped"}


class UserTable(BaseTable):
    username = columns.Column(linkify=True)
    date_joined = columns.DateTimeColumn(format="d/m/y")
    created = None

    class Meta:
        model = User
        fields = ("username", "date_joined", "last_login", "is_active", "is_staff", "is_superuser")
        attrs = {"class": "table key-buttons border-bottom"}