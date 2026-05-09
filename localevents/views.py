from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from .forms import EventCreateForm
from .models import Event, EventSignup

class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html' 
    context_object_name = 'all_events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            
            organized = Event.objects.filter(organizer=profile)
            signed_up = Event.objects.filter(eventsignup__user_registrant=profile)
            
            context['organized_events'] = organized
            context['signed_up_events'] = signed_up
            
            context['all_events'] = Event.objects.exclude(organizer=profile).exclude(eventsignup__user_registrant=profile)
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventCreateForm
    template_name = 'localevents/event_form.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        event = form.save()
        event.organizer.add(self.request.user.profile)
        return response

class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = ['title', 'category', 'event_image', 'description', 'location', 'start_time', 'end_time', 'event_capacity', 'status']
    template_name = 'localevents/event_form.html'

    def form_valid(self, form):
        event = form.save(commit=False)

        selected_status = form.cleaned_data.get('status')

        if selected_status not in ['Cancelled', 'Done']:
            signup_count = event.eventsignup_set.count()
            if signup_count >= event.event_capacity:
                event.status = 'Full'
            else:
                event.status = 'Available'
        else:
            event.status = selected_status

        return super().form_valid(form)

def event_signup(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.user.is_authenticated:
        EventSignup.objects.get_or_create(event=event, user_registrant=request.user.profile)
        return redirect('localevents:event-detail', pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            EventSignup.objects.create(event=event, new_registrant=name)
            return redirect('localevents:event-detail', pk=pk)
            
    return render(request, 'localevents/event_signup_form.html', {'event': event})
