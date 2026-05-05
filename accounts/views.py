from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Profile

from .forms import ProfileUpdateForm
# Create your views here.

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profile_update.html'
    

    def get_object(self, queryset=None):
        return self.request.user.profile