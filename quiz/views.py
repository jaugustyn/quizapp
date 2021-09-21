from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework import generics
from .models import Category, Question, Answer, Quiz
from .serializers import CategorySerializer, QuizSerializer, QuestionSerializer, AnswerSerializer


# Create your views here.

# Future endpoints?
# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'categories': reverse('category_list', request=request, format=format)
#     })


@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Category List': '/categories/',
        'Quiz Detail': '/categories/<slug:slug>/',
        'Quiz Result': '/categories/<slug:slug>/quizzes/',
    }
    return Response(api_urls)


class category_list(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# class category_detail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.filter()
#     lookup_field = 'slug'
#     serializer_class = CategorySerializer


@api_view(['GET','POST'])
def quiz_list(request, slug):
    if request.method == "GET":
        quizzes = list(Quiz.objects.filter(category_id=slug).values_list('question', flat=True))
        questions = Question.objects.filter(id__in=quizzes)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def quiz_result(request, slug):
    if request.method == "POST":
        pass


# @api_view(['POST'])
# def category_update(request, pk):
#     quiz = Category.objects.get(pk=pk)
#     serializer = CategorySerializer(instance=quiz, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors)
