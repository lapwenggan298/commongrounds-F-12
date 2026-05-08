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


