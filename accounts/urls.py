from django.urls import path
from .views import register, login, logout, account_home, profile_edit, change_pwd

urlpatterns = [
    path('register', register, name="register"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    path('dashboard/', account_home, name="dashboard"),
    path('dashboard/profile_edit', profile_edit, name="profile_edit"),
    path('dashboard/change_pwd', change_pwd, name="change_pwd"),
]