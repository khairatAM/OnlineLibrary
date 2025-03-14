from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from .models import Book
from datetime import date, timedelta

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def create_book(request):
    if request.user.is_librarian == False:
        return redirect('books:books_list')        
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
    if request.user.is_librarian == False:
        return redirect('books:books_list')  

    book = get_object_or_404(Book, pk=id)      
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book.save()
            return redirect('books:books_list') 
    else:
        form = BookForm(instance=book)

    return render(request, 'book_edit.html', {'form': form, 'book': book})

@login_required
def book_checkout(request, id):
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
    book = get_object_or_404(Book, pk=id)
    if book.reader is None:
        return redirect('books:book_detail', id=id) 

    book.reader = None
    book.date_checked_out = None
    book.expected_return_date = None
    book.save()

    # Schedule an email reminder to the reader
    # check_in_reminder_email(book.reader.email, book.title, book.expected_return_date)
    
    return redirect('books:book_detail', id=id) 

@login_required
def books_list_checked_out(request):
    if request.user.is_librarian == False:
        return redirect('books:books_list')
    books = Book.objects.filter(reader__isnull=False)
    return render(request, 'books_checked_out.html', {'books': books})

@login_required
def books_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(isbn__icontains=query) | Book.objects.filter(publisher__icontains=query) | Book.objects.filter(added_date__icontains=query) if query else []
    return render(request, 'books_search.html', {'books': books})

@login_required
def book_reader(request, id):
    if request.user.is_librarian == False:
        return redirect('books:book_detail', id=id) 

    book = get_object_or_404(Book, pk=id)
    if book.reader is not None:
        days_till_due = (book.expected_return_date - date.today()).days
        return render(request, 'book_reader.html', {'book': book, 'days_till_due': days_till_due})

    return redirect('books:book_detail', id=id)

@login_required
def check_in_reminder_email(email, title, expected_return_date):
    subject = 'Return Book Reminder Email'
    message = f'This is a reminder that you have to return the book with title { title } back by { expected_return_date }.'
    recipient_email = email

    # Example: Date when the email should be sent (e.g., 2 minutes from now)
    send_date = timezone.now() + timedelta(minutes=2)

    # Schedule the email with Celery
    send_reader_email.apply_async(args=[subject, message, recipient_email, send_date], eta=send_date)

    return render(request, 'your_template.html', {'send_date': send_date})