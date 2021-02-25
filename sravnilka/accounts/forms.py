from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    UserChangeForm
from django.forms import CharField, TextInput, PasswordInput, EmailField
from .models import User


class CustomUserCreationFormAdmin(UserCreationForm):
    """Форма создания юзера для админки"""
    class Meta(UserCreationForm):
        model = User
        fields = ('email', )


class CustomUserChangeFormAdmin(UserChangeForm):
    """Форма изменения данных юзера для админки"""
    class Meta:
        model = User
        fields = ('email',)


class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации пользователя"""
    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username', 'password1', 'password2')
        widgets = {
            'email': TextInput(),
            'username': TextInput(),
            'password1': PasswordInput(),
            'password2': PasswordInput()
        }


class LoginUserForm(AuthenticationForm):
    """Форма для входа"""
    username = EmailField(label='Почта', widget=TextInput())
    password = CharField(label='Пароль', widget=PasswordInput())
