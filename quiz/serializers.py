from rest_framework import serializers
from .models import Category, Question, Answer, Quiz


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
        lookup_field = 'name'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['answer1', 'answer2', 'answer3', 'answer4', 'correct_answer', ]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer()

    class Meta:
        model = Question
        fields = ['question', 'points', 'answers']


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['description', 'category']
        lookup_field = 'category'
        depth = 1
