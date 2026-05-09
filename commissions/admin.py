from django.contrib import admin
from .models import Commission, CommissionType, Job, JobApplication


class CommissionInLine(admin.StackedInline):
    model = Commission
    extra = 0


class JobApplicationInLine(admin.TabularInline):
    model = JobApplication
    extra = 0


class JobInLine(admin.StackedInline):
    model = Job
    extra = 0


@admin.register(CommissionType)
class CommissionTypeAdmin(admin.ModelAdmin):
    inlines = [CommissionInLine]
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    inlines = [JobInLine,]
    list_display = (
        "title",
        "maker",
        "type",
        "people_required",
        "created_on",
        "updated_on",
    )
    search_fields = ("title",)
    list_filter = ("created_on", "type",)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    inlines = [JobApplicationInLine]
    list_display = (
        "role",
        "commission",
        "status",
        "manpower_required",
    )
    list_filter = ("status",)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "applicant",
        "job",
        "status",
    )
    list_filter = ("status", "job",)