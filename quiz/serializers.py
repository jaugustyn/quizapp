from rest_framework import serializers
from .models import Category, Question, Answer, Quiz


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        lookup_field = 'name'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        # fields = ['answer1', 'answer2', 'answer3', 'answer4', 'correct_answer']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer()

    class Meta:
        model = Question
        # fields = ['question', 'points', 'answers']
        fields = "__all__"


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        # fields = ['description', 'category']
        fields = "__all__"
        lookup_field = 'category'
        depth = 1
