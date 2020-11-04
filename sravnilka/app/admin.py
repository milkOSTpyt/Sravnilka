from django.contrib import admin
from .models import Books


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):

    list_display = ('pk', 'shop', 'title', 'author', 'price')
    list_display_links = ('pk', 'title',)
    search_fields = ('title', )
    #list_filter = ('title', 'price')
    empty_value_display = '-'


admin.site.site_header = 'Админка'