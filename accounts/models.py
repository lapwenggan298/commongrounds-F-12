from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()

    ROLE_CHOICES = [
        ("MEMBER", "Member"),
        ("MARKET_SELLER", "Market Seller"),
        ("EVENT_ORGANIZER", "Event Organizer"),
        ("BOOK_CONTRIBUTOR", "Book Contributor"),
        ("PROJECT_CREATOR", "Project Creator"),
        ("COMMISSION_MAKER", "Commission Maker"),
    ]

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="MEMBER",
    )

    class Meta:
        ordering = ['user__username']
        
    def __str__(self):
        return self.display_name or self.user.username