from django.db import models
from django.db.models import Case, When, IntegerField


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Commission(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("FULL", "Full"),
        ("COMPLETED", "Completed"),
        ("DISCONTINUED", "Discontinued"),
    ]
    
    type = models.ForeignKey(
        "CommissionType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions",
    )

    maker = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,)
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    def get_queryset(self):
        return Commission.objects.annotate(
        status_order=Case(
            When(status="OPEN", then=0),
            When(status="FULL", then=1),
            When(status="COMPLETED", then=2),
            When(status="DISCONTINUED", then=3),
            output_field=IntegerField(),
        )
        ).order_by("status_order", "-created_on")

    def __str__(self) -> str:
        return self.title
    
class Job(models.Model):
    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("FULL", "Full"),
    ]

    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name="jobs",
    )

    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    class Meta:
        ordering = ["-status", "-manpower_required", "role"]

    def __str__(self):
        return self.role


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications",
    )

    applicant = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING",
    )

    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
        Case(
            When(status="PENDING", then=0),
            When(status="ACCEPTED", then=1),
            When(status="REJECTED", then=2),
            output_field=IntegerField(),
        ),
        "-applied_on",
        ]
        