from django.db import models
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year_of_publication = models.IntegerField()
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title
    
    
class UserProfile(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    date_registered = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username