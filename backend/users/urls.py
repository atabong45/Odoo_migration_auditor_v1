# users/urls.py
from django.urls import path
from .views import UserCreateView, CurrentUserView, UserProfileUpdateView, ChangePasswordView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='register'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('password/change/', ChangePasswordView.as_view(), name='password-change'),
]