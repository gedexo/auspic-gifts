# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, UpdateView, DeleteView,CreateView

# forms
from accounts.forms import CustomerAddressForm

# models
from accounts.models import CustomerAddress
from order.models import Order

from .forms import CustomUserChangeForm


class AddAddress(View):
    def post(self, request):
        user = request.user
        form = CustomerAddressForm(request.POST)
        if form.is_valid():
            address_type = form.cleaned_data.get("address_type")
            is_default = form.cleaned_data.get("is_default")
            if CustomerAddress.objects.filter(customer=user).exists():
                if is_default == True:
                    CustomerAddress.objects.filter(customer=user).update(
                        is_default=False
                    )
                if CustomerAddress.objects.filter(
                    customer=user, address_type=address_type
                ).exists():
                    CustomerAddress.objects.filter(
                        customer=user, address_type=address_type
                    ).update(**form.cleaned_data)
                else:
                    CustomerAddress.objects.filter(customer=user).create(
                        **form.cleaned_data, customer=user
                    )
                response_data = {
                    "status": "true",
                    "title": "Successfully Submitted",
                    "message": "Address Updated successfully.",
                }
                return JsonResponse(response_data)
            else:
                form.save(commit=False).customer = user
                form.save()
                response_data = {
                    "status": "true",
                    "title": "Successfully Submitted",
                    "message": "Address added successfully.",
                }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return JsonResponse(response_data)


class AddressListView(LoginRequiredMixin, ListView):
    model = CustomerAddress
    template_name = "account/address.html"
    context_object_name = "address"

    def get_queryset(self):
        # Filter orders based on the currently logged-in user
        return CustomerAddress.objects.filter(customer=self.request.user)[:2]

    extra_context = {"my_address": True, "form": CustomerAddressForm()}


def get_address_data(request):
    address_id = request.GET.get("address_id")
    print("address_id=", address_id)
    address = get_object_or_404(CustomerAddress, id=address_id)
    print("address=", address)
    data = {
        "full_name": address.full_name,
        "mobile_no": address.mobile_no,
        "district": address.district.id,
        "city": address.city,
        "address_line_1": address.address_line_1,
        "address_line_2": address.address_line_2,
        "state": address.state.id,
        "pin_code": address.pin_code,
        "is_default": address.is_default,
    }
    return JsonResponse(data)


def customer_address_edit(request, pk):
    address = get_object_or_404(CustomerAddress, pk=pk)
    user = request.user
    if request.method == "POST":
        form = CustomerAddressForm(request.POST, instance=address)
        if form.is_valid():
            address_type = form.cleaned_data.get("address_type")
            is_default = form.cleaned_data.get("is_default")
            print("is_default", is_default)
            if CustomerAddress.objects.filter(
                customer=user, address_type=address_type
            ).exists():
                CustomerAddress.objects.filter(
                    customer=user, address_type=address_type
                ).update(**form.cleaned_data)
            else:
                form.instance.customer = request.user
                form.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Address Updated successfully.",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
            }
        return JsonResponse(response_data)


def delete_address(request, pk):
    address = get_object_or_404(CustomerAddress, pk=pk)
    address.delete()
    response_data = {
        "status": "true",
        "title": "Successfully Submitted",
        "message": "Address deleted successfully.",
    }
    return JsonResponse(response_data)


class SettingView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "account/settings.html"
    success_url = reverse_lazy("accounts:setting")
    extra_context = {"my_setting": True}

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Settings updated successfully.",
        }
        return JsonResponse(response_data)


class UserOrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "account/orders.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        # Filter orders based on the currently logged-in user
        return Order.objects.filter(user=self.request.user, is_ordered=True)

    extra_context = {"my_order": True}


class UserOrderDetailView(DetailView):
    model = Order
    template_name = "account/order_single.html"
    context_object_name = "order"
    slug_field = "order_id"  # Use 'order_id' as the slug field
    slug_url_kwarg = "order_id"

    extra_context = {"my_order": True}



from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from registration.backends.default.views import RegistrationView

from main import mixins

from . import tables
from .forms import CustomRegistrationForm
from .models import User


class CustomRegistrationView(RegistrationView):
    form_class = CustomRegistrationForm
    success_url = reverse_lazy('web:index') 

    def register(self, form):
        user = form.save(commit=False)
        user.mobile_number = form.cleaned_data['mobile_number']    
        user.save()

        # Authenticate and login the user
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
        
        return user


class UserListView(ListView):
    model = User
    table_class = tables.UserTable
    filterset_fields = ("is_active", "is_staff")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Users"
        context["can_add"] = True
        context["new_link"] = reverse_lazy("accounts:user_create")
        return context


class UserDetailView(DetailView):
    model = User


class UserCreateView(CreateView):
    model = User
    exclude = ("is_active", "date_joined", "user_permissions", "groups", "last_login", "is_superuser", "is_staff")

    def form_valid(self, form):
        form.instance.set_password(form.cleaned_data["password"])
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    model = User
    exclude = (
        "is_active",
        "password",
        "date_joined",
        "user_permissions",
        "groups",
        "last_login",
        "is_superuser",
        "is_staff",
    )


class UserDeleteView(DeleteView):
    model = User