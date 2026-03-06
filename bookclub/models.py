from django.db import models
from django.urls import reverse
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField()
    publication_year = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    book_category = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='genres',
    )

    def __str__(self):
        return f"{self.title} by {self.author} published in {self.publication_year} of the genre {self.book_category.name}."
    
    def get_absolute_url(self):
        return reverse("bookclub:book_detail", args=[str(self.pk)])

    class Meta:
        ordering = ['-publication_year']

