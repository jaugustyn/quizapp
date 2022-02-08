import random
import unittest

from rest_framework import viewsets, mixins
from rest_framework.views import APIView, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .models import Category, Question, Quiz
from .serializers import CategorySerializer, QuestionSerializer, QuestionAdminSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, extend_schema_view


# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    lookup_field = "name"  # For URLs
    filter_backends = [OrderingFilter]
    ordering_fields = ['name']
    ordering = "name"  # Default

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Creates quiz with this category name
        quiz = Quiz.objects.create(category_id=request.data['name'], description=f"{request.data['name']} quiz")
        quiz.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Updates questions and quiz category, but requires foreign_key checks set to 0 to work properly (its included in settings)
        Quiz.objects.filter(category_id=instance.name).update(category_id=request.data["name"])
        Question.objects.filter(category=instance).update(category=request.data["name"])

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(parameters=[OpenApiParameter("category", OpenApiTypes.STR, OpenApiParameter.QUERY)])
)
class QuestionViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]
    serializer_class = QuestionSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        queryset = Question.objects.filter(approved=True)
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category_id=category)

            #  If category doesn't exist then return all questions
            if not queryset.exists():
                return Question.objects.filter(approved=True)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Adds question to the quiz from chosen category
        if request.data['category'] is not None:
            quiz = Quiz.objects.get(category_id=request.data['category'])
            question = Question.objects.get(pk=serializer.data['id'])
            quiz.question.add(question)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @unittest.skip("Don't want to test")
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Updates question category
        old_quiz = Quiz.objects.get(question=instance.id)
        question_old = Question.objects.get(id=instance.id)
        old_quiz.question.remove(question_old)  # Removes old version of question from quiz

        if instance.category is not None:
            quiz = Quiz.objects.get(category_id=request.data['category'])
            question = Question.objects.get(pk=serializer.data["id"])
            quiz.question.add(question)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class NewQuestionSuggestion(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(approved=False)


@extend_schema_view(
    list=extend_schema(parameters=[OpenApiParameter("category", OpenApiTypes.STR, OpenApiParameter.QUERY)],
                       operation_id="suggestion_list")
)
class QuestionDraftList(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = QuestionAdminSerializer
    permission_classes = [IsAdminUser]

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


class SingleQuestionDraft(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = Question.objects.filter(approved=False)
    serializer_class = QuestionAdminSerializer
    permission_classes = [IsAdminUser]

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
        if request.data["approved"]:
            quiz = Quiz.objects.get(category_id=request.data['category'])
            question = Question.objects.get(pk=serializer.data['id'])
            quiz.question.add(question)

        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[OpenApiParameter("limit", OpenApiTypes.INT, OpenApiParameter.QUERY)],
    description="Limit - amount of questions, Name - category of the quiz"
)
class GetQuiz(APIView):
    serializer_class = None
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, name, format=None):
        amount_of_questions = request.GET.get('limit', "2")  # Query filter
        try:
            ids_list = list(Quiz.objects.values_list('question', flat=True).filter(category_id=name))
            if not ids_list:
                return Response({"message": "The quiz with the given category name does not exist"},
                                status=status.HTTP_404_NOT_FOUND)

            if int(amount_of_questions) > len(ids_list):  # If someone wants more questions than are in DB then return just 1 question
                choosen_set = random.sample(ids_list, k=1)
            else:
                choosen_set = random.sample(ids_list, k=int(amount_of_questions))

            questions = Question.objects.filter(id__in=choosen_set)
            serializer = QuestionSerializer(questions, many=True)

        except ValueError:
            return Response({"message": "ValueError - Wrong limit value in query filter"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
