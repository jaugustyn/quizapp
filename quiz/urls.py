from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<str:name>/', views.question_from_category, name='category_name')
]
