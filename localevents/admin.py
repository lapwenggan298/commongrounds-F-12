from django.contrib import admin
from .models import Event, EventType

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ('name', )
    search_fields = ('name', )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'category'
        'description'
        'location'
    )
    search_fields = (
        'title',
        'location',
        'description'
    )




# Register your models here.
