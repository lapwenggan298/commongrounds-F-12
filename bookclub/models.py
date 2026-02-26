from django.db import models
from django.urls import reverse
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name',]



class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField()
    publication_year = models.IntegerField()
    created_on = models.DateTimeField()
    updated_on = models.DateTimeField()

    bookcategory = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genres',
    )

    def __str__(self):
        return f"{self.title} by {self.author} published in {self.publication_year} of the genre {self.bookcategory.name}."
    
    def get_absolute_url(self):
        return reverse("bookclub:book_detail", args=[str(self.id)])

    class Meta:
        ordering = ['-publication_year',]