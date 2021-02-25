from django.utils.safestring import mark_safe
from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationFormAdmin, CustomUserChangeFormAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFormAdmin
    form = CustomUserChangeFormAdmin
    model = User
    list_display = ('pk', 'username', 'email', 'is_superuser', 'created_at',
                    'get_photo')
    list_display_links = ('pk', 'email', 'username')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('get_photo', 'created_at', 'last_login')
    fieldsets = (
        ('Общее', {'fields': ('email', 'username', 'first_name',
                              'last_name', 'phone', 'password', 'created_at',
                              'last_login')}),
        ('Фото', {'fields': ('avatar', 'get_photo')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_admin',
                                    'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2',
                       'is_superuser', 'is_staff', 'is_active', 'is_admin')}
         ),
    )
    search_fields = ('email', 'username')
    ordering = ('created_at',)

    def get_photo(self, obj):
        """ Функция выводит в админку фото """
        default = "https://alyans-meb73.ru/images/faces/avatar.png"
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" width="65">')
        return mark_safe(f'<img src={default} width="65">')

    get_photo.short_description = 'Фото'
