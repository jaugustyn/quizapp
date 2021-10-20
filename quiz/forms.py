from django import forms
from .views import Question, Answer
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms.models import inlineformset_factory


class AnswersForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["answer1", "answer2", "answer3", "answer4", "correct_answer"]


class QuestionForm(forms.ModelForm):
    answers = AnswersForm

    class Meta:
        model = Question
        fields = ['question', 'points']


QuestionFormSet = inlineformset_factory(
    Answer,
    Question,
    fields='__all__',
)
