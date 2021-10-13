from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Category, Question, Quiz, Answer
from .serializers import CategorySerializer, QuestionSerializer
import random


# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    lookup_field = "name"


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


@api_view(['GET'])
def quiz_list(request, name):
    if request.method == "GET":
        amount_of_questions = request.GET.get('limit', "2")
        ids_list = list(Quiz.objects.values_list('question', flat=True).filter(category_id=name))
        choosen_set = random.sample(ids_list, k=int(amount_of_questions))
        questions = Question.objects.filter(id__in=choosen_set)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)
