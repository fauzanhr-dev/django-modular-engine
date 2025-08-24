from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from engine_modular.decorators import require_installed
from .models import Product


# Public R (view) — no login required for list
@method_decorator(require_installed("product_module"), name="dispatch")
class ProductListView(ListView):
    model = Product
    template_name = "product_module/product_list.html"
    context_object_name = "products"


# User CRU (here: C & U need login + perms)
@method_decorator(
    [login_required, permission_required("product_module.add_product")], name="dispatch"
)
@method_decorator(require_installed("product_module"), name="dispatch")
class ProductCreateView(CreateView):
    model = Product
    fields = ["name", "barcode", "price", "stock"]
    template_name = "product_module/product_form.html"
    success_url = reverse_lazy("product_module:product_list")


@method_decorator(
    [login_required, permission_required("product_module.change_product")],
    name="dispatch",
)
@method_decorator(require_installed("product_module"), name="dispatch")
class ProductUpdateView(UpdateView):
    model = Product
    fields = ["name", "barcode", "price", "stock"]
    template_name = "product_module/product_form.html"
    success_url = reverse_lazy("product_module:product_list")


# Manager CRUD: delete requires delete permission
@method_decorator(
    [login_required, permission_required("product_module.delete_product")],
    name="dispatch",
)
@method_decorator(require_installed("product_module"), name="dispatch")
class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_module/product_confirm_delete.html"
    success_url = reverse_lazy("product_module:product_list")
