from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter
from app.models import Book
from .serializers import BookSerializer


class BookListView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'author']
    filter_backends = (SearchFilter,)
    http_method_names = ['get']
