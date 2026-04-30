from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

class ProductType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    class Meta:
        ordering = ['name']
            

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    type = models.ForeignKey(
        "ProductType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name= "products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        ordering = ['name']
            

    def __str__(self):
        return self.name
    