from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Profile
from merchstore.models import Product
from localevents.models import Event
from bookclub.models import Book
from diyprojects.models import Project
from commissions.models import Commission

from .forms import ProfileUpdateForm
# Create your views here.

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile_update.html'
    
    success_url = reverse_lazy('accounts:profile_dashboard')

    def get_object(self, queryset=None):
        return self.request.user.profile
    

class ProfileDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        user = self.request.user

        ctx['products'] = Product.objects.filter(owner=user)
        ctx['events'] = Event.objects.filter(organizer=user)
        ctx['books'] = Book.objects.filter(contributor=user)
        ctx['projects'] = Project.objects.filter(creator=user)
        ctx['commissions'] = Commission.object.filter(maker=user)

        return ctx
    

class HomeView(TemplateView):
    template_name = 'home.html'