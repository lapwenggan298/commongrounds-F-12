from django.contrib import admin
from .models import Event, EventType, EventSignup


class EventSignupInLine(admin.StackedInline):
    model = EventSignup
    extra = 0


class EventInLine(admin.TabularInline):
    model = Event
    extra = 0


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    inlines = [EventInLine]
    list_display = ('name',) 
    ordering = ('name',) 
    search_fields = ('name',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [EventSignupInLine]
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