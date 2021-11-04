from django.core.validators import validate_image_file_extension, validate_slug
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from .models import Category, Question, Answer, Quiz


class CategorySerializer(serializers.ModelSerializer):
    category_url = serializers.SlugField(source='slug', validators=[validate_slug])
    image = serializers.ImageField(use_url=True, allow_null=True, validators=[validate_image_file_extension])

    class Meta:
        model = Category
        fields = ["id", "name", "image", "category_url", "color", "description"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "answer1", "answer2", "answer3", "answer4", "correct_answer"]


class QuestionSerializer(WritableNestedModelSerializer):
    answers = AnswerSerializer(many=False)

    class Meta:
        model = Question
        fields = ['id', 'question', 'points', 'answers', 'category']


class QuestionSerializerAdmin(WritableNestedModelSerializer):
    answers = AnswerSerializer(many=False)
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question', 'points', 'answers', 'category', 'approved']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = "__all__"
        # depth = 1
