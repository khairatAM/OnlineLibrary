# accounts/views.py
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django import urls
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import logout

User = get_user_model()

def create_default_admin(request):
    user = User.objects.create_user('admin001', 'admin001@test.com', 'Password123')
    user.is_librarian = True
    user.save()

def logout_view(request):
    logout(request)
    return redirect('users:login')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_reader = True
            user.save()
            return redirect('users:login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def admin_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_librarian = True
            user.save()
            return redirect('users:login')  # Redirect to the login page after successful registration
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})
