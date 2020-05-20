from django.urls import path
from .views import index, booklist,author_detail_view, book_detail_view, all_borrowed_books, authorlist, onloan_book_list, all_users, renew_book_librarian, author_create,author_update,author_delete, book_create, book_delete, book_update, create_bookinstance, update_bookinstance, delete_bookinstance
urlpatterns =[
    path("",  index, name="index"),
    path("all-users/",  all_users, name="all-users"),
    path('books/', booklist, name='books'),
    path('authors/', authorlist, name='authors'),
    path('book/<int:pk>', book_detail_view, name='book-detail'),
    path('author/<int:id>', author_detail_view, name='author-detail'),
    path('mybooks/', onloan_book_list, name='my-borrowed'),
    path('myborrowed/', all_borrowed_books, name='all-borrowed'),
    path('book/<uuid:pk>/renew/', renew_book_librarian, name='renew-book-librarian'),
    path('book-instance/<uuid:pk>/', create_bookinstance, name='book-instance'),

    ]
urlpatterns += [
    path('author/create/', author_create.as_view(), name='author_create'),
    path('author/<int:pk>/update/', author_update.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', author_delete.as_view(), name='author_delete'),
    path('book/create/', book_create.as_view(), name='book_create'),
    path('book/<int:pk>/update/', book_update.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', book_delete.as_view(), name='book_delete'),
]
