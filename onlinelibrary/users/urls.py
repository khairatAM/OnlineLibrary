from django.urls import path

# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "users"
urlpatterns = [
    path('create-default-admin/', views.create_default_admin, name='create_default_admin'),

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin/register/', views.admin_register, name='admin-register'),
    path('admin/login/', LoginView.as_view(), name='login'),
]
