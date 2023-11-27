from django.urls import path
from .views import BookList, UserCreate

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('users/register/', UserCreate.as_view(), name='user-register')
]