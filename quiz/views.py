import random
from django.shortcuts import render
from .models import Category, Question


# Create your views here.

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'quiz/base.html', {'categories': categories})


def question_from_category(request, name):
    ids_list = list(Question.objects.values_list('id', flat=True).filter(category_id=name))
    choosen_set = random.sample(ids_list, k=3)
    quiz = Question.objects.filter(id__in=choosen_set)

    return render(request, 'quiz/question_list.html', {'quiz': quiz})
