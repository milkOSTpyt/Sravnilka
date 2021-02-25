from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import LoginUserForm, CustomUserCreationForm
from django.contrib.auth.views import LoginView, LogoutView


class LoginUser(LoginView):
    """Вход"""
    form_class = LoginUserForm
    template_name = 'accounts/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    """Регистрация"""
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Регистрация'}


class LogoutUser(LogoutView):
    """Выход"""
    next_page = 'home'

