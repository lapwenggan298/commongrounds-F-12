from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.display_name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()

    # ROLE_CHOICES = [
    #     ("MEMBER", "Member"),
    #     ("MARKET_SELLER", "Market Seller"),
    #     ("EVENT_ORGANIZER", "Event Organizer"),
    #     ("BOOK_CONTRIBUTOR", "Book Contributor"),
    #     ("PROJECT_CREATOR", "Project Creator"),
    #     ("COMMISSION_MAKER", "Commission Maker"),
    # ]

    roles = models.ManyToManyField(
        Role,
        related_name='profiles',
        blank=True,
    )

    def __str__(self):
        return self.display_name or self.user.username

    class Meta:
        ordering = ['user__username']


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, display_name=instance.username)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()