from django.shortcuts import render
from django.views.generic import ListView
from.models import Books
from django.db.models import Q

def index(request):
    '''Главная функция'''
    search = request.GET.get('q', '')
    if search:
        s = Books.objects.filter(Q(title__icontains=search) | Q(author__icontains=search))
        context = {
            'search': s,
            'title' : search,
        }
        return render(request, 'app/search.html', context)

    else:
        return render(request, 'app/index.html')
        
