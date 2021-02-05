from app.models import Book
from rest_framework.serializers import ModelSerializer


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        exclude = ('img_link', )


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ('shop', )
