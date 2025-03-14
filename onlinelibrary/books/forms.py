from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'cover_image', 
            'title', 
            'isbn', 
            'revision_number', 
            'published_date', 
            'publisher', 
            'author', 
            'added_date', 
            'genre',
            ]
