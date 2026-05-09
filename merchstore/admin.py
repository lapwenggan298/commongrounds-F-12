from django.contrib import admin
from .models import Product, ProductType, Transaction

# Register your models here.

class ProductInLine(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [ProductInLine]
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "stock",
        "status",
        "owner",
    )
    search_fields = ("name",)
    list_filter = ("status", "type",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "buyer",
        "amount",
        "status",
        "created_on",
    )
    list_filter = ("status",)
    search_fields = ("product__name", "buyer__user__username",)
