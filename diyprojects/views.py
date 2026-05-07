from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Avg
from .models import Project, Favorite, ProjectReview, ProjectRating

class ProjectListView(ListView):
    model = Project
    template_name = "diyprojects/project_list.html"
    context_object_name = "projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            
            created = Project.objects.filter(creator=profile)
            favorited = Favorite.objects.filter(profile=profile)
            reviewed = ProjectReview.objects.filter(reviewer=profile)

            created_ids = created.values_list("id", flat=True)
            favorited_ids = favorited.values_list("project_id", flat=True)
            reviewed_ids = reviewed.values_list("project_id", flat=True)
            
            context['created_projects'] = created
            context['favorites'] = favorited
            context['reviews'] = reviewed
            
            context['all_projects'] = Project.objects.exclude(
                    id__in=created_ids
                ).exclude(
                    id__in=favorited_ids
                ).exclude(
                    id__in=reviewed_ids
                )      
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "diyprojects/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        average = ProjectRating.objects.filter(
                project=self.object
            ).aggregate(avg=Avg('score'))['avg']
        context['average_score'] = average

        favorite_count = Favorite.objects.filter(
            project=self.object
            ).count()
        context['favorite_count'] = favorite_count

        return context
