from django import forms

from .models import Order
from datetime import date, timedelta


class OrderForm(forms.ModelForm):
    selected_dial_code_mobile = forms.CharField(widget=forms.HiddenInput(), required=False)
    selected_dial_code_alternative = forms.CharField(widget=forms.HiddenInput(), required=False)
    gift_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"placeholder": "Enter Gift Card Code"}))

    DELIVERY_DATE_CHOICES = [
        ("today", "Today"),
        ("tomorrow", "Tomorrow"),
        ("select_date", "Select a Date"),
    ]
    delivery_date_choice = forms.ChoiceField(
        choices=DELIVERY_DATE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "time-slot-radio"})
    )
    
    selected_date = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "id": "datepicker", "placeholder": "Select a Date"})
    )

    TIME_SLOT_CHOICES = [
        ("9-12", "9:00 AM - 12:00 PM"),
        ("12-6", "12:00 PM - 6:00 PM"),
    ]
    time_slot = forms.ChoiceField(
        choices=TIME_SLOT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "time-slot-radio"})
    )

    class Meta:
        model = Order
        fields = [
            "full_name", "address_line_1", "address_line_2",
            "mobile_no", "state", "district", "city",
            "pin_code", "email", "gift_code", "delivery_date_choice",
            "selected_date", "time_slot"
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "address_line_1": forms.TextInput(attrs={"class": "form-control", "placeholder": "House/Floor No. Building Name or Street, Locality"}),
            "address_line_2": forms.TextInput(attrs={"class": "form-control", "placeholder": "Any nearby landmark"}),
            "mobile_no": forms.TextInput(attrs={"class": "form-control", "placeholder": "Mobile No", "type": "tel", "maxlength": "10"}),
            "state": forms.TextInput(attrs={"class": "form-control", "placeholder": "State"}),
            "district": forms.TextInput(attrs={"class": "form-control", "placeholder": "District"}),
            "city": forms.TextInput(attrs={"class": "form-control", "placeholder": "City"}),
            "pin_code": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pin Code"}),
            "email": forms.TextInput(attrs={"class": "form-control", "placeholder": "Email", "type": "email"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        delivery_date_choice = cleaned_data.get("delivery_date_choice")
        selected_date = cleaned_data.get("selected_date")
        time_slot = cleaned_data.get("time_slot")

        if delivery_date_choice == "select_date" and not selected_date:
            self.add_error("selected_date", "Please select a date.")

        if not time_slot:
            self.add_error("time_slot", "Please select a time slot.")

        return cleaned_data

class TrackingForm(forms.Form):
    tracking_id = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"placeholder": "Tracking id"})
    )
