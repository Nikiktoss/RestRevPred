from django.urls import path
from .views import UserLoginView, main, UserCreateView, UserDetailView, UserUpdateView, CalculationForm, \
    send_pdf_file, send_json_file
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', UserLoginView.as_view(), name="login_page"),
    path('main/', main, name="main_page"),
    path('logout/', LogoutView.as_view(next_page='login_page'), name="logout"),
    path('sign_up/', UserCreateView.as_view(), name="sign_up_page"),
    path('profile/<slug:slug>/', UserDetailView.as_view(), name="profile_page"),
    path('profile/<slug:slug>/edit/', UserUpdateView.as_view(), name="edit_profile_page"),
    path('predict/', CalculationForm.as_view(), name="predict_revenue_form"),
    path('send_pdf/<int:pk>/', send_pdf_file, name="send_pdf_file"),
    path('send_json/<int:pk>/', send_json_file, name="send_json_file"),
]
