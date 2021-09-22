from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework import generics, status
from .models import Category, Question, Answer, Quiz
from .serializers import CategorySerializer, QuizSerializer, QuestionSerializer, AnswerSerializer


# Create your views here.


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Api Overview': "/",
        'Category List': 'categories/',
        'Quiz Detail': 'questions/<category_name>/',
    }
    return Response(api_urls)


class category_list(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class category_update(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    lookup_url_kwarg = "name"
    lookup_field = "name"


# @api_view(['GET', 'POST', "PUT", "DELETE"])
# def category_crud(request, pk):
#     quiz = Category.objects.get(pk=pk)
#     serializer = CategorySerializer(instance=quiz, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)


@api_view(['GET'])
def quiz_list(request, slug):
    if request.method == "GET":
        quizzes = list(Quiz.objects.filter(category_id=slug).values_list('question', flat=True))
        questions = Question.objects.filter(id__in=quizzes)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)



