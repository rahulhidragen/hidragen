# myapp/urls.py
from django.urls import path
from .views import hello_world, create_user, fetch_user, create_category, fetch_category, create_product, fetch_product, update_product, login, delete_category

urlpatterns = [
    path('hello/', hello_world, name='hello_world'),
    path('create/user/', create_user, name='create_user'),
    path('fetch/user/', fetch_user, name='fetch_user'),
    path('create/category/', create_category, name='create_category'),
    path('fetch/category/', fetch_category, name='fetch_category'),
    path('delete/category/', delete_category, name='delete_category'),
    path('create/product/', create_product, name='create_product'),
    path('fetch/product/', fetch_product, name='fetch_product'),
    path('update/product/', update_product, name='update_product'),
    path('login/', login, name='login'),
]
