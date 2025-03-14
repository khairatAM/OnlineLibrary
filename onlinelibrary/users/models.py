# importing necessary django classes
from django.db import models
from django.contrib.auth.models import AbstractUser

# User class
class User(AbstractUser):
	# User fields
	profile_photo = models.ImageField(upload_to='images/profile', null=True)
	is_librarian = models.BooleanField(default=False)
	is_reader = models.BooleanField(default=False)