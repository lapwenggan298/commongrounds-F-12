from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Project

class ProjectListView(ListView):
    model = Project
    template_name = "diyprojects/"

class ProjectDetailView(DetailView):
    model = Project
    template_name = "diyprojects/"