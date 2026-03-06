from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path("item/", ProductListView.as_view(), name="product_list"),
    path("item/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),

]


app_name = "merchstore"