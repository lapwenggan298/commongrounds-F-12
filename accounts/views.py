from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy

from .models import Profile
from merchstore.models import Product
from localevents.models import Event
from bookclub.models import Book
from diyprojects.models import Project
from commissions.models import Commission

from .forms import ProfileUpdateForm, ProfileCreateForm
# Create your views here.

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile_update.html'
    
    success_url = reverse_lazy('accounts:profile_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.profile
    

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    
    success_url = reverse_lazy('accounts:profile_create')

    def form_valid(self, form):
        result = super().form_valid(form)
       
        login(self.request, self.object)
        return result


class ProfileCreateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileCreateForm
    template_name = 'profile_create.html'

    success_url = reverse_lazy('accounts:profile_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.profile


class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user_profile = self.request.user.profile

        ctx['products'] = Product.objects.filter(owner=user_profile)
        ctx['events'] = Event.objects.filter(organizer=user_profile)
        ctx['books'] = Book.objects.filter(contributor=user_profile)
        ctx['projects'] = Project.objects.filter(creator=user_profile)
        ctx['commissions'] = Commission.objects.filter(maker=user_profile)

        return ctx
        

class HomeView(TemplateView):
    template_name = 'home.html'