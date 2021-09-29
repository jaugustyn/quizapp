import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from .serializers import *


# Create your tests here.


class QuestionTestCase(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'id': 1,
            'answers': {"answer1": "test_1", "answer2": "test_2", "answer3": "test_3", "answer4": "test_4",
                        "correct_answer": "1"},
            'question': "Does test passed?",
            'points': 3
        }
        self.question = QuestionSerializer(data=self.data)
        if self.question.is_valid():
            self.question.save()
        self.client = APIClient()

    def test_create_question(self):
        self.data = {
            'id': 1,
            'answers': {"answer1": "test_1", "answer2": "test_2", "answer3": "test_3", "answer4": "test_4",
                        "correct_answer": "1"},
            'question': "Does test passed?",
            'points': 3
        }
        response = self.client.post('/questions/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_question(self):
        questions = Question.objects.get(pk=1)
        response = self.client.get('/questions/', args={'pk': questions.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, questions)
