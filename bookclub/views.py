from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Book
# Create your views here.

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'