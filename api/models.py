from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLES_CHOICES, default='user')

    def __str__(self):
        return self.username
    
class FavoriteCat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='favorite_cats')
    cat_id = models.CharField(max_length=15)  # ID del gato de The Cat API
    image_url = models.URLField()  # URL de la imagen del gato

    def __str__(self):
        return f"{self.user.username} - {self.cat_id}"