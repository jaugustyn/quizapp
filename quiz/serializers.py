from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Category, Question, Answer, Quiz


class CategorySerializer(serializers.ModelSerializer):
    category_url = serializers.SlugField(source='slug')
    image = serializers.ImageField(use_url=True, max_length=None)

    class Meta:
        model = Category
        fields = ["id", "name", "image", "category_url"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionSerializer(WritableNestedModelSerializer):
    answers = AnswerSerializer()

    class Meta:
        model = Question
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        depth = 1
