from django.urls import path
from .views import BookListView, ShopListView


urlpatterns = [
    path('', BookListView.as_view()),
    path('shops/', ShopListView.as_view()),
]
