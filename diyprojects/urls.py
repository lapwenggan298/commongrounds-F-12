from django.urls import path
from . import views
from .views import ProjectListView, ProjectDetailView

urlpatterns = [
    path(
        "projects/", 
        ProjectListView.as_view(), 
        name="project_list"
    ), 
    path(
        "project/<int:pk>", 
        ProjectDetailView.as_view(), 
        name="project_detail"
    ), 
    path(
        "project/<int:pk>/favorite",
        views.add_favorite, 
        name="add_favorite"
    ), 
    path(
        "project/<int:pk>/rate/", 
        views.add_rating, 
        name="add_rating"
    ), 
    path(
        "project/<int:pk>/review/", 
        views.add_review, 
        name="add_review"
    ), 
]

app_name = "diyprojects"
