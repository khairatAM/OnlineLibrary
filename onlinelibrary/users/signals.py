from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_migrate)
def create_default_admin(**kwargs):
    if not User.objects.filter(username='admin001').exists():
        User.objects.create_user(
            username='admin001', 
            email='admin001@test.com', 
            password='Password123',
            is_librarian=True,
            )