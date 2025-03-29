from django.urls import path
from . import views

app_name = "books"
urlpatterns = [
    path('', views.home, name='home'),
    path('list', views.books_list, name='books_list'),
    path('checked-out', views.books_list_checked_out, name='books_list_checked_out'),
    path('search', views.books_search, name='books_search'),
    path('create', views.create_book, name='create_book'),
    path('<int:id>/detail', views.book_detail, name='book_detail'),
    path('<int:id>/edit', views.book_edit, name='book_edit'),
    path('<int:id>/checkout', views.book_checkout, name='book_checkout'),
    path('<int:id>/checkin', views.book_checkin, name='book_checkin'),
    path('<int:id>/reader', views.book_reader, name='book_reader'),
]
