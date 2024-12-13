from django.urls import path
from .views import RegisterView, LoginView, LogoutView, account_home, ProfileEditView, ChangePasswordView


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('dashboard/profile_edit/', ProfileEditView.as_view(), name="profile_edit"),
    path('dashboard/change_pwd/', ChangePasswordView.as_view(), name="change_pwd"),
    path('dashboard/', account_home, name="dashboard"),

]