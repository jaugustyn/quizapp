from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins, status
from .models import Category, Question, Quiz, Answer
from .serializers import CategorySerializer, QuestionSerializer, QuizSerializer
from .forms import QuestionForm, AnswersForm,  QuestionFormSet
import random
from rest_framework.renderers import TemplateHTMLRenderer


# Create your views here.

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    lookup_field = "name"


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# class QuizViewSet(viewsets.ModelViewSet):
#     queryset = Quiz.objects.all()
#     serializer_class = QuizSerializer


@api_view(['GET'])
def quiz_list(request, name):
    if request.method == "GET":
        amount_of_questions = request.GET.get('limit', "2")
        ids_list = list(Quiz.objects.values_list('question', flat=True).filter(category_id=name, question__approved=True))
        choosen_set = random.sample(ids_list, k=int(amount_of_questions))
        questions = Question.objects.filter(id__in=choosen_set)

        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class NewQuestion(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(approved=False)

    # def post(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = QuestionSerializer(queryset, many=False)
    #     return Response(serializer.data)

    # if request.method == "POST":
    #     form = QuestionForm(request.POST)
    #     if form.is_valid():
    #         question = form.save(commit=False)
    #         question.save()
    #         return question


class QuestionDraftList(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(approved=False)
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(quiz__category_id=category)
        return queryset


