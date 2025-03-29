from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from .models import Book
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseForbidden

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def create_book(request):
    # Ensure that only librarians can access this view
    if request.user.is_librarian == False:
        return HttpResponseForbidden("You do not have permission to view this resource.")       
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('books:books_list') 
    else:
        form = BookForm()

    return render(request, 'create_books.html', {'form': form})

@login_required
def books_list(request):
    books = Book.objects.all()
    return render(request, 'books_list.html', {'books': books})

@login_required
def book_detail(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def book_edit(request, id):
    # Ensure that only librarians can access this view
    if request.user.is_librarian == False:
        return HttpResponseForbidden("You do not have permission to view this resource.")         

    book = get_object_or_404(Book, pk=id)      
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books:book_detail', id=id) 
    else:
        form = BookForm(instance=book)

    return render(request, 'book_edit.html', {'form': form, 'book': book})

@login_required
def book_checkout(request, id):
    # Ensure that only readers can access this view
    if request.user.is_reader == False:
        return HttpResponseForbidden("You do not have permission to view this resource.")      

    book = get_object_or_404(Book, pk=id)
    if book.reader is not None:
        return redirect('books:books_list') 

    book.reader = request.user
    book.date_checked_out = date.today()
    book.expected_return_date = book.date_checked_out + timedelta(days=10)
    book.save()
    return redirect('books:book_detail', id=id) 

@login_required
def book_checkin(request, id):
    # Ensure that only readers can access this view
    if request.user.is_reader == False:
        return HttpResponseForbidden("You do not have permission to view this resource.") 
    
    book = get_object_or_404(Book, pk=id)
    if book.reader is None:
        return redirect('books:book_detail', id=id) 

    book.reader = None
    book.date_checked_out = None
    book.expected_return_date = None
    book.save()
    
    return redirect('books:book_detail', id=id) 

@login_required
def books_list_checked_out(request):
    # Ensure that only librarians can access this view
    if request.user.is_librarian == False:
        return HttpResponseForbidden("You do not have permission to view this resource.")       
    
    books = Book.objects.filter(reader__isnull=False)
    return render(request, 'books_checked_out.html', {'books': books})

@login_required
def books_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(isbn__icontains=query) | Book.objects.filter(publisher__icontains=query) | Book.objects.filter(added_date__icontains=query) if query else []
    return render(request, 'books_search.html', {'books': books})

@login_required
def book_reader(request, id):
    # Ensure that only librarians can access this view
    if request.user.is_librarian == False:
        return HttpResponseForbidden("You do not have permission to view this resource.")       

    book = get_object_or_404(Book, pk=id)
    if book.reader is not None:
        days_till_due = (book.expected_return_date - date.today()).days
        return render(request, 'book_reader.html', {'book': book, 'days_till_due': days_till_due})

    return redirect('books:book_detail', id=id)
