from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordResetDoneView
)
from .views import LoginUser, RegisterUser, LogoutUser


urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('pass-reset/',
         PasswordResetView.as_view(
             template_name='accounts/pass-reset.html'),
         name='pass-reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html',),
         name='password_reset_done'),
]
