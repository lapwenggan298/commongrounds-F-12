from django.db import models
from django.urls import reverse



class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Event(models.Model):
    category = models.ForeignKey(
        EventType, on_delete=models.SET_NULL,
        null = True, 
        related_name = "events")
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time =models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created_on']
        
    
    def __str__(self):
        return self.title


# Create your models here.
