from celery import shared_task
from django.core.mail import send_mail
from .models import Book
from datetime import date
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def send_checkin_reminder_email(recipient, book_title):
    subject = 'Book Return Reminder'
    message = f'''Dear Reader, 
    This is a reminder that you have two days to return the book with title {book_title}.
    '''
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False,)
        print(f"Check In Reminder sent to {recipient}!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

def send_book_overdue_email(reader_email, book_id, book_title, expected_return_date, recipient_admin_email='admin001@gmail.com'):
    subject = 'Book Overdue'
    message = f'''Dear Admin,
    This is a reminder that the book with id {book_id}, titled {book_title} and borrowed by the user with email {reader_email}, has not been returned by the expected return date of {expected_return_date}.
    '''
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [recipient_admin_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False,)
        print(f"Book Overdue Notification sent to {recipient_admin_email}.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

@shared_task
def check_borrowed_books():
    books = Book.objects.filter(reader__isnull=False)
    for book in books:
        days_till_due = (book.expected_return_date - date.today()).days
        if days_till_due == 2:
            send_checkin_reminder_email(recipient=book.reader.email, book_title=book.title)
            print(f"Check In Reminder sent to {book.reader.email}!")


@shared_task
def check_overdue_books():
    books = Book.objects.filter(reader__isnull=False)
    for book in books:
        days_till_due = (book.expected_return_date - date.today()).days
        print(days_till_due)
        if days_till_due <= 0:
            send_book_overdue_email(
                reader_email=book.reader.email, 
                book_id=book.id,
                book_title=book.title,
                expected_return_date=book.expected_return_date,
                )
            print(f"Book overdue sent to admin, {book.reader.email}!")
    