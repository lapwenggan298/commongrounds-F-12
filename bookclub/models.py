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
    synopsis = models.TextField(blank=True)
    available_to_borrow = models.BooleanField()

    contributor = models.ForeignKey(
       'accounts.Profile',
       on_delete=models.SET_NULL,
       null=True,
       related_name='books_contributed_to',
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
    )

    def __str__(self):
        return f"{self.title} by {self.author} published in {self.publication_year} of the genre {self.genre.name}."
    
    def get_absolute_url(self):
        return reverse("bookclub:book_detail", args=[str(self.pk)])

    class Meta:
        ordering = ['-publication_year']


class BookReview(models.Model):
    title = models.CharField()
    anon_reviewer = models.TextField(blank=True)
    comment = models.TextField(blank=True)

    user_review = models.ForeignKey(
       'accounts.Profile',
       on_delete=models.CASCADE,
       null=True,
       blank=True,
       related_name='book_reviews',
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
    )


class Bookmark(models.Model):
    date_bookmarked = models.DateField()

    profile = models.ForeignKey(
       'accounts.Profile',
       on_delete=models.CASCADE,
       related_name='books_bookmarked',
       null=True,
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='bookmarks',
    )


class Borrow(models.Model):
    date_borrowed = models.DateField()
    date_to_return = models.DateField()
    name = models.CharField()

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrowed',
    )

    borrower = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='borrowed_books',
    )
