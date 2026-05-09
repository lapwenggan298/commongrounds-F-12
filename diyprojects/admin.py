from django.contrib import admin
from .models import Project, ProjectCategory, Favorite, ProjectReview, ProjectRating


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1
    fields = ("title", "creator", "description",)


class ProjectReviewInLine(admin.StackedInline):
    model = ProjectReview
    extra = 0


class ProjectRatingInLine(admin.TabularInline):
    model = ProjectRating
    extra = 0


class FavoriteInLine(admin.TabularInline):
    model = Favorite
    extra = 0


class ProjectCategoryAdmin(admin.ModelAdmin):
    model = ProjectCategory
    inlines = [ProjectInline]
    list_display = ("name", "description", )
    ordering = ("name", )
    search_fields = ("name", )


class ProjectAdmin(admin.ModelAdmin):
    model = Project
    inlines = [ProjectReviewInLine, ProjectRatingInLine, FavoriteInLine]
    list_display = (
        "title", 
        "category", 
        "description", 
        "created_on", 
        "updated_on", 
    )
    search_fields = ("title", )
    list_filter = ("created_on", "category", )


class FavoriteAdmin(admin.ModelAdmin):
    model = Favorite
    list_display = (
        "project", 
        "profile", 
        "date_favorited", 
        "project_status", 
    )
    ordering = ("date_favorited", )


class ProjectReviewAdmin(admin.ModelAdmin):
    model = ProjectReview
    list_display = (
        "project", 
        "reviewer", 
        "comment", 
        "image", 
    )
    ordering = ("project", )

class ProjectRatingAdmin(admin.ModelAdmin):
    model = ProjectRating
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
