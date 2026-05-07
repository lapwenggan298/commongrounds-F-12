from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class ProjectCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Project categories"

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        "ProjectCategory", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="projects", 
    )
    creator = models.ForeignKey(
        "accounts.Profile", 
        on_delete=models.CASCADE, 
    )
    description = models.TextField()
    materials = models.TextField()
    steps = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self) -> str:
        return self.title
    
class Favorite(models.Model):
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE, 
    )
    profile = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
    )
    date_favorited = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('Backlog', 'Backlog'),
        ('To-Do', 'To-Do'),
        ('Done', 'Done'),
    ]
    project_status = models.CharField(choices=status_choices,default='Backlog')

class ProjectReview(models.Model):
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE, 
    )
    reviewer = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    image = models.ImageField()

class ProjectRating(models.Model):
    profile = models.ForeignKey(
        "accounts.Profile",
        on_delete=models.CASCADE
    )
    score = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)])
