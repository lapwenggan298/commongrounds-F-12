from django.contrib import admin
from .models import Event, EventType, EventSignup

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',) 
    ordering = ('name',) 
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category',
        'status',   
        'event_capacity', 
        'start_time',
        'location',
    )
    list_filter = ('status', 'category')
    search_fields = (
        'title',
        'location',
        'description',
    )

@admin.register(EventSignup)
class EventSignupAdmin(admin.ModelAdmin):
    list_display = ('event', 'user_registrant', 'new_registrant')