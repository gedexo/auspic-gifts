from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from accounts.models import CustomerAddress


class CustomerAddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        exclude = ("customer",)

    widgets = {
        "address_type": forms.RadioSelect(
            attrs={"class": "form-control", "placeholder": "Address Type"}
        ),
        "full_name": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Full name"}
        ),
        "mobile_no": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Mobile No", "type": "tel"}
        ),
        "district": forms.Select(
            attrs={"class": "form-control", "placeholder": "District"}
        ),
        "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
        "address": forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Address Line"}
        ),
        "pin_code": forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Zip Code"}
        ),
        "is_default": forms.CheckboxInput(attrs={"class": "form-check-input"}),
    }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        exclude = ("password",)


from django import forms
from registration.forms import RegistrationForm
from .models import User


class CustomRegistrationForm(RegistrationForm):
    mobile_number = forms.CharField(max_length=128, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email',"mobile_number", 'password1', 'password2']
