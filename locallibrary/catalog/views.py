from django.shortcuts import render
from django.views import generic
from .models import Book, BookInstance, Author, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from .forms import RenewBookForm
from datetime import date
import datetime
from django.shortcuts import reverse
from django.http import HttpResponseRedirect

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# class BookListView(generic.ListView):
#     model = Book

#     queryset = Book.objects.all()
#     print(queryset)
#     context_object_name = 'book_list'
#     template_name='book/booklist.html'

#     def get_context_data(self, **kwargs):
#         context = super(BookListView, self).get_context_data(**kwargs)

#         context['book_list'] = self.queryset
#         return context

@staff_member_required
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method=="POST":
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
        return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date = date.today()+datetime.timedelta(weeks=3)
        form = RenewBookForm(initial = {'renewal_date':proposed_renewal_date})
        context = {
        'form':form,
        'book_instance':book_instance,
        }
        return render(request, 'book/book_renew_librarian.html', context)


from django.shortcuts import get_object_or_404
@login_required(login_url="catalog/")
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk = pk)
    return render(request, 'book/book_detail.html', {'book':book })


@login_required(login_url="catalog/")
def booklist(request):
    book_list = Book.objects.all()
    length = len(book_list)
    return render(request, 'book/booklist.html', {'book_list':book_list,'length':length})



@login_required(login_url="catalog/")
def author_detail_view(request, id):
    author = get_object_or_404(Author, id = id)
    books_by_author = Book.objects.filter(author__exact=author
        )
    print(books_by_author)

    return render(request, 'book/author_detail.html', {'author':author, 'books_by_author':books_by_author})


@login_required(login_url="catalog/")
def authorlist(request):
    author_list = Author.objects.all()
    length = len(author_list)
    return render(request, 'book/authorlist.html', {'author_list':author_list,'length':length})


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
    'num_books':num_books,
    'num_instances':num_instances,
    'num_instances_available': num_instances_available,
    'num_authors':num_authors,
    }

    return render(request, 'index.html', context = context)

@login_required(login_url="catalog/")
def onloan_book_list(request):
    obj = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('due_back')
    return render(request, "book/onloan_book_list.html", {'obj':obj})


@staff_member_required
def all_borrowed_books(request):
    obj = BookInstance.objects.filter(status__exact='o').order_by('due_back')
    print(obj)
    return render(request, "book/staff_onloans_list.html", {'obj':obj})

@staff_member_required
def all_users(request):
    obj = User.objects.all()
    print(obj)
    return render(request, "book/users_list.html", {'obj':obj})


class  author_create(CreateView):
    model = Author
    fields = "__all__"
    template_name="book/author_form.html"



class  author_update(UpdateView):
    model = Author
    fields = {'first_name', 'last_name','date_of_birth','date_of_death'}

    template_name="book/author_form.html"



class  author_delete(DeleteView):
    model = Author
    template_name="book/author_confirm_delete.html"
    success_url = reverse_lazy("authors")


class  create_bookinstance(CreateView):
    model = BookInstance
    fields = "__all__"
    template_name="book/bookinstance_form.html"



class  update_bookinstance(UpdateView):
    model = BookInstance
    fields = {'book', 'imprint','status','due_back', 'borrower'}

    template_name="book/bookinstance_form.html"



class  delete_bookinstance(DeleteView):
    model = BookInstance
    template_name="book/bookinstance_confirm_delete.html"
    success_url = reverse_lazy("my-borrowed")

class  book_create(CreateView):
    model = Book
    fields = "__all__"
    template_name="book/book_form.html"


class  book_update(UpdateView):
    model = Book
    fields = { 'id','title','author','genre','summary'}


    template_name="book/book_form.html"



class  book_delete(DeleteView):
    model = Book
    template_name="book/author_confirm_delete.html"
    success_url = reverse_lazy("books")
