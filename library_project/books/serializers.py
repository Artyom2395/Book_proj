from rest_framework import serializers
from .models import Book, UserProfile

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'date_registered')
        read_only_fields = ('date_registered',)