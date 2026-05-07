from django.contrib import admin
from .models import Project, ProjectCategory, Favorite


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


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    inline = [ProjectInline]
    list_display = (
        "project", 
        "profile", 
        "date_favorited", 
        "project_status", 
    )
    ordering = ("date_favorited", )


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Favorite, FavoriteAdmin)
