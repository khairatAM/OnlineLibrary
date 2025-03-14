from django.db import models
from datetime import date
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Book(models.Model):
    cover_image = models.ImageField(upload_to='images/books')
    title = models.CharField(max_length=500)
    isbn = models.CharField(max_length=500)
    revision_number = models.IntegerField()
    published_date = models.DateField(default=date(2000, 1, 1))
    publisher = models.CharField(max_length=1000)
    author = models.TextField()
    added_date = models.DateField(default=date.today)
    genre = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reader = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    date_checked_out = models.DateTimeField(null=True)
    expected_return_date = models.DateField(null=True)
