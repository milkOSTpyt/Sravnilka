from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import ListView
from.models import Book


class HomePage(View):
    """ Главная страница сайта с поисковым полем """
    def get(self, request):
        return render(request, 'app/index.html')


class Search(ListView):
    """ Поиск книг """
    paginate_by = 21
    template_name = 'app/search.html'
    context_object_name = 'book_list'

    def get_queryset(self):
        search = self.request.GET.get('q', '')
        return Book.objects.filter(Q(title__icontains=search) | Q(
                                                    author__icontains=search))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        context["title"] = self.request.GET.get("q")
        return context
