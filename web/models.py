from django.db import models
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField

from .base import BaseModel
from .choices import BANNER_POSITION_CHOICE


class Banner(BaseModel):
    position = models.CharField(max_length=50, choices=BANNER_POSITION_CHOICE)
    banner_image = ThumbnailerImageField(
        upload_to="banners/", help_text="Main :1980 × 821 ,  others : 787 × 300"
    )
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
        ordering = ("id",)


class Contact(BaseModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(
        max_length=15,
    )
    place = models.CharField(
        max_length=120,
    )
    message = models.TextField()
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.full_name())

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
