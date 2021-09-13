from django.shortcuts import render
from .models import Category, Question


# Create your views here.

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/base.html', {'categories': categories})
