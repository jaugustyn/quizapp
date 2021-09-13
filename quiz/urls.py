from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list')
]
