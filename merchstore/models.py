from django.db import models
from django.urls import reverse


class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("ON_SALE", "On sale"),
        ("OUT_OF_STOCK", "Out of stock"),
    ]

    type = models.ForeignKey(
        ProductType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    owner = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=255)
    product_image = models.ImageField(upload_to="merchstore/", blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="AVAILABLE",
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("merchstore:product_detail", kwargs={"pk": self.pk})

    def update_status_from_stock(self):
        if self.stock == 0:
            self.status = "OUT_OF_STOCK"
        elif self.status == "OUT_OF_STOCK":
            self.status = "AVAILABLE"

    @property
    def is_owned_by(self, profile):
        return self.owner_id == getattr(profile, "id", None)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("ON_CART", "On cart"),
        ("TO_PAY", "To Pay"),
        ("TO_SHIP", "To Ship"),
        ("TO_RECEIVE", "To Receive"),
        ("DELIVERED", "Delivered"),
    ]

    buyer = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="transactions",
    )
    amount = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ON_CART",
    )
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        buyer_name = self.buyer.display_name if self.buyer else "Unknown"
        return f"{buyer_name} - {self.product.name} ({self.amount})"
    