from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "merchstore/product_list.html"
    context_object_name = "merchstore"

class ProductDetailView(DetailView):
    model = Product
    template_name = "merchstore/product_detail.html"
    context_object_name = "product"