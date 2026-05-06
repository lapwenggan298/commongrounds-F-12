from collections import defaultdict

from django import forms
from accounts.mixins import RoleRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product, Transaction


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["owner"]
        widgets = {
            "stock": forms.NumberInput(attrs={"min": 0}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": 0}),
        }


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ["owner"]
        widgets = {
            "stock": forms.NumberInput(attrs={"min": 0}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": 0}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount"]
        widgets = {
            "amount": forms.NumberInput(attrs={"min": 1}),
        }


class ProductListView(ListView):
    model = Product
    template_name = "merchstore/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.select_related("owner", "type").all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        queryset = self.get_queryset()

        if user.is_authenticated and hasattr(user, "profile"):
            profile = user.profile
            my_products = queryset.filter(owner=profile)
            other_products = queryset.exclude(pk__in=my_products.values_list("pk", flat=True))
            context["my_products"] = my_products
            context["products"] = other_products
        else:
            context["products"] = queryset

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = kwargs.get("form", TransactionForm())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")

        if not hasattr(request.user, "profile"):
            return redirect('login')

        profile = request.user.profile
        if self.object.owner_id == profile.id:
            form = TransactionForm(request.POST)
            form.add_error(None, "You cannot purchase your own product.")
            return self.render_to_response(self.get_context_data(form=form))

        if self.object.stock == 0:
            form = TransactionForm(request.POST)
            form.add_error(None, "This product is out of stock.")
            return self.render_to_response(self.get_context_data(form=form))

        form = TransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]
            if amount > self.object.stock:
                form.add_error("amount", "The requested amount exceeds available stock.")
                return self.render_to_response(self.get_context_data(form=form))

            transaction = form.save(commit=False)
            transaction.buyer = profile
            transaction.product = self.object
            transaction.save()

            self.object.stock -= amount
            self.object.update_status_from_stock()
            self.object.save(update_fields=["stock", "status"])
            return redirect("merchstore:cart")

        return self.render_to_response(self.get_context_data(form=form))


class ProductCreateView(RoleRequiredMixin, CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "merchstore/product_form.html"
    required_role = "MARKET_SELLER"

    def form_valid(self, form):
        form.instance.owner = self.request.user.profile
        if form.instance.stock == 0:
            form.instance.status = "OUT_OF_STOCK"
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("merchstore:product_detail", kwargs={"pk": self.object.pk})


class ProductUpdateView(RoleRequiredMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name = "merchstore/product_form.html"
    required_role = "MARKET_SELLER"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("merchstore:product_list")
        product = self.get_object()
        if product.owner_id != request.user.profile.id:
            return redirect("merchstore:product_list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        product = form.instance
        if product.stock == 0:
            product.status = "OUT_OF_STOCK"
        else:
            product.status = "AVAILABLE"
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("merchstore:product_detail", kwargs={"pk": self.object.pk})



class CartView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/cart.html"
    context_object_name = "transactions"

    def get_queryset(self):
        profile = self.request.user.profile
        return Transaction.objects.select_related("product__owner", "product").filter(buyer=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped = defaultdict(list)
        for transaction in context["transactions"]:
            grouped[transaction.product.owner].append(transaction)
        context["transactions_by_owner"] = grouped.items()
        return context


class TransactionListView(RoleRequiredMixin, ListView):
    model = Transaction
    template_name = "merchstore/transaction_list.html"
    context_object_name = "transactions"
    required_role = "MARKET_SELLER"

    def get_queryset(self):
        profile = self.request.user.profile
        return Transaction.objects.select_related("buyer", "product").filter(product__owner=profile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grouped = defaultdict(list)
        for transaction in context["transactions"]:
            grouped[transaction.buyer].append(transaction)
        context["transactions_by_buyer"] = grouped.items()
        return context
