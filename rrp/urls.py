from django.urls import path
from .views import UserLoginView, main, UserCreateView, UserDetailView, UserUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', UserLoginView.as_view(), name="login_page"),
    path('main/', main, name="main_page"),
    path('logout/', LogoutView.as_view(next_page='login_page'), name="logout"),
    path('sign_up/', UserCreateView.as_view(), name="sign_up_page"),
    path('profile/<slug:slug>/', UserDetailView.as_view(), name="profile_page"),
    path('profile/<slug:slug>/edit/', UserUpdateView.as_view(), name="edit_profile_page"),
]
