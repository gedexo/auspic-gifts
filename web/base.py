from django.db import models
from import_export.admin import ImportExportModelAdmin
from django.conf import settings

from .actions import mark_active, mark_inactive
from .functions import generate_fields
from django.contrib.auth import get_user_model
User=get_user_model()

class BaseModel(models.Model):
    BOOL_CHOICES = ((True, "Yes"), (False, "No"))
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="creator_%(class)s_objects",
        on_delete=models.PROTECT,
        editable=False,
    )
    is_active = models.BooleanField(
        "Mark as Active", default=True, choices=BOOL_CHOICES, blank=True
    )

    class Meta:
        abstract = True
        ordering = ["-created"]

    def get_fields(self):
        return generate_fields(self)

    # def delete(self, *args, **kwargs):
    #     self.is_active = False
    #     self.save()
    #     return HttpResponseRedirect(self.get_list_url())


class BaseAdmin(ImportExportModelAdmin):
    exclude = ["creator", "is_active"]
    list_display = ("__str__", "created", "updated", "is_active")
    list_filter = ("is_active",)
    actions = [mark_active, mark_inactive]
    readonly_fields = ("is_active", "creator", "pk")
    search_fields = ("pk",)

    def render_change_form(
        self, request, context, add=False, change=False, form_url="", obj=None
    ):
        context.update(
            {"show_save_and_continue": False, "show_save_and_add_another": False}
        )
        return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
