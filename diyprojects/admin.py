from django.contrib import admin
from .models import Project, ProjectCategory, Favorite, ProjectReview, ProjectRating


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


class ProjectReviewAdmin(admin.ModelAdmin):
    model = ProjectReview
    inline = [ProjectInline]
    list_display = (
        "project", 
        "reviewer", 
        "comment", 
        "image", 
    )
    ordering = ("project", )

class ProjectRatingAdmin(admin.ModelAdmin):
    model = ProjectRating
    inline = [ProjectInline]
    list_display = (
        "project", 
        "profile", 
        "score", 
    )

admin.site.register(ProjectCategory, ProjectCategoryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ProjectReview, ProjectReviewAdmin)
admin.site.register(ProjectRating, ProjectRatingAdmin)
