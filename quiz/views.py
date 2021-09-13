from django.shortcuts import render
from .models import Category, Question


# Create your views here.

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/base.html', {'categories': categories})


def question_from_category(request, name):
    quiz = Question.objects.filter(category_id=name)
    return render(request, 'quiz/question_list.html', {'quiz': quiz})
