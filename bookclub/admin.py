from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import Genre, Book, BookReview, Bookmark, Borrow
# Register your models here.

class BookInLine(admin.TabularInline):
    model = Book


class BookmarkInLine(admin.TabularInline):
    model = Bookmark
    extra = 0


class BookReviewInLine(admin.TabularInline):
    model = BookReview
    extra = 1
    fields = [
        'title', 
        'user_review', 
        'anon_reviewer', 
        'comment',
        ]
    readonly_fields = [
        'user_review',
        'anon_reviewer'
    ]


class BorrowInLine(admin.TabularInline):
    model = Borrow
    extra = 0
    fields = [
        'name',
        'date_borrowed',
        'date_to_return',
    ]
    readonly_fields = [
        'date_borrowed',
        'date_to_return',
    ]
    def status_tag(self, obj):
        if obj.date_to_return < timezone.now().date():
            return format_html('<b style="color:red;">OVERDUE</b>')
        return "Active"
    status_tag.short_description = 'Status'


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
    inlines = [BookReviewInLine, BookmarkInLine, BorrowInLine,]
    search_fields = [
        'title',
        'author',
        'genre',
        'publication_year',
        'available_to_borrow',
    ]
    list_display = [
        'title',
        'author',
        'genre',
        'publication_year',
        'created_on',
        'updated_on',
        'available_to_borrow',
    ]
    list_filter = [
        'author',
        'genre',
        'publication_year',
        'available_to_borrow',
    ]
    fieldsets = [
        ("Book Information", {
            'fields':[
                ('title', 'author', 'genre', 'publication_year'), 'synopsis',
            ]
        }),
        ("Availability", {
            'fields':[
                ('available_to_borrow', 'contributor')
            ]
        }),
        ("Miscellaneous", {
            'fields':[
                ('created_on', 'updated_on')
            ]
        }),
    ]
    readonly_fields = [
        'created_on',
        'updated_on',
        ]


class BorrowAdmin(admin.ModelAdmin):
    list_display = [
        'book',
        'display_borrower',
        'date_borrowed',
        'date_to_return',
    ]
    list_filter = [
        'date_borrowed',
        'date_to_return',
    ]

    def display_borrower(self, obj):
        if obj.borrower:
            return f"Member: {obj.borrower.display_name}"
        return f"Guest: {obj.name}"
    display_borrower.short_description = 'Borrower'


admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(Bookmark)
admin.site.register(BookReview)