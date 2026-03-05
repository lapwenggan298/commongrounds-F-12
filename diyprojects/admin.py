from django.contrib import admin
from .models import Project, ProjectCategory


class ProjectInline(admin.TabularInline):
    model = Project


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inline = [ProjectInline]
    list_display = ("name", "description", )
    ordering = ("name", )
    search_fields = ("name", )


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = (
        "title", 
        "category", 
        "description", 
        "materials", 
        "steps", 
        "created_on", 
        "updated_on", 
    )
    search_fields = ("title", )
    list_filter = ("created_on", "category", )  


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
