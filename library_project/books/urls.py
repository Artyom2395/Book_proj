from django.urls import path
from .views import BookList, UserCreate, BookDetail

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('users/register/', UserCreate.as_view(), name='user-register')
]