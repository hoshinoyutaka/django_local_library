import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, BookInstance, Author, Genre, Language
from .forms import RenewBookForm

# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_books_algebra = Book.objects.filter(title__icontains='algebra').count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,        
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_books_algebra': num_books_algebra,
        'num_visits': num_visits,
    }
    return render(request, 'catalog/index.html', context)

class BookListView(ListView):
    model = Book
    ordering = 'id'
    paginate_by = 20

class BookDetailView(DetailView):
    model = Book

class AuthorListView(ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(borrower=self.request.user).filter(status__exact='o')

# Permissions for BookInstance views are done like that:
# Either we decorate @permission_required('catalog.can_mark_returned')
# Or we inherit from PermissionRequiredMixin and set permission_required = ('catalog.can_mark_returned',)
class BorrowedBooksListView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    # View is visible only for Librarians user group
    permission_required = ('catalog.can_mark_returned',)
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(status__exact='o')

class RenewBookLibrarian(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_mark_returned'

    def get(self, request, *args, **kwargs):
        book_instance = get_object_or_404(BookInstance, pk=self.kwargs['pk'])
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        context = {
            'form': form, 
            'book_instance': book_instance,
        }
        return render(request, 'catalog/renew_book_librarian.html', context)

    def post(self, request, *args, **kwargs):
        book_instance = get_object_or_404(BookInstance, pk=self.kwargs['pk'])
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
            
        context = {
            'form': form, 
            'book_instance': book_instance,
        }
        return render(request, 'catalog/renew_book_librarian.html', context)
    
class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': datetime.date.today()}

class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('author-list')

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']

class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('book-list')