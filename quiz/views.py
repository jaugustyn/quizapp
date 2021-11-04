import random

from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Category, Question, Quiz, Answer
from .serializers import CategorySerializer, QuestionSerializer, QuestionSerializerAdmin


# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    lookup_field = "name"  # For URLs

    filter_backends = [OrderingFilter]
    ordering_fields = ['name']
    ordering = "name"  # Default


class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.filter(approved=True)
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category_id=category)

            #  If category doesn't exist then return all questions
            if not queryset.exists():
                return Question.objects.filter(approved=True)
        return queryset


class NewQuestionSuggestion(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save(approved=False)


class QuestionDraftList(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionSerializerAdmin
    filter_backends = [OrderingFilter]
    ordering_fields = ['category']

    def get_queryset(self):
        queryset = Question.objects.filter(approved=False)
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category_id=category)
            if not queryset.exists():
                return Question.objects.filter(approved=False)
        return queryset


class SingleQuestionDraft(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.filter(approved=False)
    serializer_class = QuestionSerializerAdmin

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        # Adds approved question to the quiz from selected category
        if 'approved' in request.data:
            quiz = Quiz.objects.get(category_id=request.data['category'])
            question = Question.objects.get(pk=serializer.data['id'])
            quiz.question.add(question)

        return Response(serializer.data)


@api_view(['GET'])
def get_quiz(request, name):
    if request.method == "GET":
        amount_of_questions = request.GET.get('limit', "2")  # Query filter
        try:
            ids_list = list(Quiz.objects.values_list('question', flat=True).filter(category_id=name))
            if not ids_list:
                return Response("The quiz with the given category name does not exist")

            if int(amount_of_questions) > len(ids_list):
                choosen_set = random.sample(ids_list, k=int(len(ids_list)))  # All questions
            else:
                choosen_set = random.sample(ids_list, k=int(amount_of_questions))

            questions = Question.objects.filter(id__in=choosen_set)
            serializer = QuestionSerializer(questions, many=True)

        except ValueError:
            return Response("Exception: Wrong limit value")

        return Response(serializer.data)
