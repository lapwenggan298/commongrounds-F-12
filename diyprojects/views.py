from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.db.models import Avg
from .models import Project, Favorite, ProjectReview, ProjectRating


@login_required
def add_favorite(request, pk):
        project = get_object_or_404(Project, pk=pk)
        profile = request.user.profile

        favorite = Favorite.objects.filter(
            profile=profile,
            project=project
        )

        if favorite.exists():
            favorite.delete()
        else:
            Favorite.objects.create(
                profile=profile,
                project=project
            )

        return redirect("diyprojects:project_detail", pk=pk)

@login_required
def add_rating(request, pk):
    project = get_object_or_404(Project, pk=pk)
    profile = request.user.profile

    if request.method == "POST":
        score = request.POST.get("score")

        ProjectRating.objects.update_or_create(
            profile=profile,
            project=project,
            defaults={
                "score": score
            }
        )

    return redirect("diyprojects:project_detail", pk=pk)

@login_required
def add_review(request, pk):
    project = get_object_or_404(Project, pk=pk)
    profile = request.user.profile

    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            ProjectReview.objects.create(
                project=project,
                reviewer=profile,
                comment=text
            )

    return redirect("diyprojects:project_detail", pk=pk)

class ProjectListView(ListView):
    model = Project
    template_name = "diyprojects/project_list.html"
    context_object_name = "all_projects"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            context['is_creator'] = profile.roles.filter(name="PROJECT_CREATOR").exists()
            
            created = Project.objects.filter(creator=profile)
            favorited = Favorite.objects.filter(profile=profile).select_related('project')
            reviewed = Project.objects.filter(project_reviews__reviewer=profile).distinct()
            
            context['created_projects'] = created
            context['favorites'] = favorited
            context['reviews'] = reviewed
        
            exclude_ids =list(created.values_list('id', flat=True)) + list(favorited.values_list('id', flat=True)) + list(reviewed.values_list('id', flat=True))

            context['all_projects'] = Project.objects.exclude(id__in=exclude_ids)
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

        is_favorited = False
        is_creator = False

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            is_creator = profile.roles.filter(name="PROJECT_CREATOR").exists()

            is_favorited = Favorite.objects.filter(
                profile=profile,
                project=self.object
            ).exists()

        context['is_favorited'] = is_favorited
        context['is_creator'] = is_creator

        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = 'diyprojects/create_project.html'
    success_url = reverse_lazy("diyprojects:project_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user.profile
        return super().form_valid(form)
    
    def test_func(self):
        return self.request.user.profile.roles.filter(name="PROJECT_CREATOR").exists()

    
class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'category', 'description', 'materials', 'steps']
    template_name = "diyprojects/edit_project.html"

    def get_success_url(self):
        return reverse_lazy("diyprojects:project_detail", kwargs={"pk": self.object.pk})
    
    def test_func(self):
        return self.request.user.profile.roles.filter(name="PROJECT_CREATOR").exists()