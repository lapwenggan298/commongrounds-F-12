from django.urls import path
from . import views 

app_name = "localevents" 

urlpatterns = [
  
    path('events', views.EventListView.as_view(), name='event-list'),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event-detail'),
    
    path('event/add', views.EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/edit', views.EventUpdateView.as_view(), name='event-update'),
    
    path('event/<int:pk>/signup', views.event_signup, name='event-signup'),
]