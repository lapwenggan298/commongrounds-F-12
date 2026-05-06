from django.contrib import admin

from .models import Genre, Book
# Register your models here.

class BookInLine(admin.TabularInline):
    model = Book


class GenreAdmin(admin.ModelAdmin):
    model = Genre
    inlines = [BookInLine]
    search_fields = [
        'name', 
    ]
    list_display = [
        'name',
        'description',
    ]
    ordering = ['name']


class BookAdmin(admin.ModelAdmin):
    model = Book
    search_fields = [
        'title',
        'author',
        'book_category',
        'publication_year',
    ]
    list_display = [
        'title',
        'author',
        'book_category',
        'publication_year',
        'created_on',
        'updated_on',
    ]
    list_filter = [
        'author',
        'book_category',
        'publication_year',
    ]
    fieldsets = [
        ("Book Information", {
            'fields':[
                ('title', 'author', 'book_category', 'publication_year')
            ]
        })
    ]


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)