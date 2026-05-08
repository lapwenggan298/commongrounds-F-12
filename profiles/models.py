from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = [
        ("MEMBER", "Member"),
        ("COMMISSION_MAKER", "Commission Maker"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    display_name = models.CharField(max_length=150, blank=True)

    role = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        default="MEMBER",
    )

    bio = models.TextField(blank=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__username"]

    def __str__(self) -> str:
        return self.display_name or self.user.username

    @property
    def is_commission_maker(self):
        return self.role == "COMMISSION_MAKER"
