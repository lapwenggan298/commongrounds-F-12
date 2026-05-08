from django.db import models
from django.urls import reverse

class EventType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Full', 'Full'),
        ('Done', 'Done'),
        ('Cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType, on_delete=models.SET_NULL,
        null=True, 
        related_name="events")
    
    organizer = models.ManyToManyField('accounts.Profile') 
    event_image = models.ImageField(upload_to='events/')
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField()
    
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='Available'
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
    
        ordering = ['-created_on'] 
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('localevents:event-detail', kwargs={'pk': self.pk})

class EventSignup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE) 
    
    user_registrant = models.ForeignKey(
        'accounts.Profile', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    ) 
    
    new_registrant = models.CharField(max_length=255, null=True, blank=True)