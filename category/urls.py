from django.urls import path
from .views import category

urlpatterns = [
    path('<slug:cat_slug>/', category, name="category"),
    path('', category, name="category_list"),
]