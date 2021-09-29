from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Category, Question, Answer, Quiz
from django.core.validators import validate_image_file_extension, validate_slug


class CategorySerializer(serializers.ModelSerializer):
    category_url = serializers.SlugField(source='slug')
    image = serializers.ImageField(use_url=True, max_length=None, validators=[validate_image_file_extension])

    class Meta:
        model = Category
        fields = ["id", "name", "image", "category_url"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["answer1", "answer2", "answer3", "answer4", "correct_answer"]


class QuestionSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    answers = AnswerSerializer(many=False)

    class Meta:
        model = Question
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        depth = 1
