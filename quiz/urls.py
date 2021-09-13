from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('<int:pk>/', views.question_from_category, name='question_from_category')
]
