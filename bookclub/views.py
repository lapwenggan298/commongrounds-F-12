from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from datetime import timedelta

from .models import Book, BookReview, Bookmark, Borrow
from .forms import BookFormFactory
from accounts.mixins import RoleRequiredMixin
# Create your views here.

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'all_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            context['book_contributor'] = (profile.role == "BOOK_CONTRIBUTOR")
            context['contributed'] = Book.objects.filter(contributor=profile)
            context['bookmarked'] = Book.objects.filter(bookmark__user=self.request.user)
            context['reviewed'] = Book.objects.filter(reviews__user_review=profile).distinct()
            
            exclude_ids = (context['contributed'] | context['bookmarked'] | context['reviewed']).values_list('id', flat=True)

            context['all_books'] = Book.objects.exclude(id__in=exclude_ids)

        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        
        form_class = BookFormFactory.getForm("review")
        profile = getattr(self.request.user, 'profile', None)
        context['review_form'] = form_class(user_profile=profile)
        
        context['bookmark_count'] = book.bookmark_set.count()
        context['is_borrowed'] = Borrow.objects.filter(book=book, returned=False).exists()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = BookFormFactory.getForm("review")
        profile = getattr(request.user, 'profile', None)
        
        form = form_class(request.POST, user_profile=profile)
        
        if form.is_valid():
            review = form.save(commit=False)
            review.book = self.object
            review.save()
            return redirect(self.object.get_absolute_url())
        
        context = self.get_context_data(object=self.object)
        context['review_form'] = form
        return self.render_to_response(context)


class BookCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):
    model = Book
    required_role = 'BOOK_CONTRIBUTOR'
    template_name = 'book_create.html'   
    
    success_url = reverse_lazy('bookclub:book_list')

    def test_func(self):
        return self.request.user.profile.role == "BOOK_CONTRIBUTOR"

    def get_form_class(self):
        return BookFormFactory.getForm("contribute")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_profile'] = self.request.user.profile
        return kwargs


class BookUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Book
    required_role = 'BOOK_CONTRIBUTOR'
    template_name = 'book_update.html'

    def get_form_class(self):
        return BookFormFactory.getForm("update")
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)

        if not request.user.is_anonymous:
            book = self.get_object()
            if book.contributor != request.user.profile:
                raise PermissionDenied("You can only edit books you contributed to.")
        
        return response

    def get_success_url(self):
        return reverse_lazy('bookclub:book_detail', kwargs={'pk':self.kwargs['pk']})


class BookBorrowView(CreateView):
    model = Borrow
    fields = ['borrower_name', 'borrow_date']
    template_name = 'book_borrow.html'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['borrower_name'] = self.request.user.profile.display_name
        return initial

    def form_valid(self, form):
        form.instance.book = Book.objects.get(pk=self.kwargs['pk'])
        
        form.instance.return_date = form.cleaned_data['borrow_date'] + timedelta(days=14)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('bookclub:book_detail', kwargs={'pk':self.kwargs['pk']})