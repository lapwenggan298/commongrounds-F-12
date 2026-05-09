from django.db import models
from django.db.models import Sum, Case, When, IntegerField


class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

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
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    type = models.ForeignKey(
        "CommissionType",
        on_delete=models.SET_NULL,
        null=True,
        related_name="commissions",
    )

    maker = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
        related_name="commissions"
        )

    people_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]


    @property
    def total_manpower_required(self):
        return self.jobs.aggregate(total=Sum('manpower_required'))['total'] or 0
    
    @property
    def open_manpower(self):
        accepted_apps = JobApplication.objects.filter(job__commission=self, status="ACCEPTED").count()
        return self.total_manpower_required - accepted_apps
    
    def update_status(self):
        jobs = self.jobs.all()
        if jobs.exists() and all(job.status == "FULL" for job in jobs):
            if self.status != "FULL":
                self.status = "FULL"
                self.save()
    
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
        ordering = [
            Case(
                When(status = "OPEN", then=0),
                When(status = "FULL", then=1),
                output_field=IntegerField()
            ),
            "-manpower_required",
            "role"
        ]
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.commission.update_status()
    
    def update_job_status(self):
        accepted = self.applications.filter(status="ACCEPTED").count()
        if accepted >= self.manpower_required:
            if self.status != "FULL":
                self.status = "FULL"
                self.save()

    def is_full(self):
        accepted = self.applications.filter(status="ACCEPTED").count()
        return accepted >= self.manpower_required        

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
        "accounts.Profile",
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

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.job.update_job_status()