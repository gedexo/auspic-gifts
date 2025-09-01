from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from django.db import models



class User(AbstractUser):
    mobile_number = models.CharField(max_length=128, blank=True, null=True)

    def get_absolute_url(self):
        return reverse_lazy("accounts:user_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("accounts:user_list")

    def get_update_url(self):
        return reverse_lazy("accounts:user_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("accounts:user_delete", kwargs={"pk": self.pk})

    @property
    def fullname(self):
        return self.username

    def __str__(self):
        return self.username


class CustomerAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address_type = models.CharField(
        max_length=10, choices=(("Home", "Home"), ("Work", "Work")), default="Home"
    )
    full_name = models.CharField(max_length=100)
    address_line_1 = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Address Line 1"
    )
    address_line_2 = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Address Line 2"
    )
    state = models.ForeignKey("main.State", on_delete=models.SET_NULL, null=True)
    district = models.ForeignKey("main.District", on_delete=models.SET_NULL, null=True)
    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=6)
    mobile_no = models.CharField(max_length=15)
    is_default = models.BooleanField(default=False, verbose_name="Set as Default")

    class Meta:
        verbose_name_plural = "CustomerAddress"

    def __str__(self):
        return str(self.customer)
