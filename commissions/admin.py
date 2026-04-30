from django.contrib import admin
from .models import Commission, CommissionType, Job, JobApplication




@admin.register(CommissionType)
class CommissionTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
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
        "applied_on",
    )

    list_filter = ("status",)

    def accept(self, request, queryset):
        queryset.update(status="ACCEPTED")
        accept.short_description = "Accept selected application"

    def reject(self, request, queryset):
        queryset.update(status="REJECTED")
        reject.short_description = "Reject selected application"

    actions = ["accept", "reject"]