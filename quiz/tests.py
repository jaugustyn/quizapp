import inspect
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from .serializers import *
from .utils import send_test_csv_report

# Create your tests here.

TEST_RESULTS = []


class QuestionTestCase(APITestCase):
    def setUp(self) -> None:
        self.answer = Answer.objects.create(id=1, answer1="test_1", answer2="test_2", answer3="test_3",
                                            answer4="test_4", correct_answer="1")
        self.question = Question.objects.create(id=1, answers_id=1, question="Does test passed?", points=3)
        self.category = Category.objects.create(name='Test', image="", slug="test", color="#FFFFFF")
        self.client = APIClient()

    def test_create_question(self):
        self.data = {
            'id': 2,
            'answers': {"answer1": "test_1", "answer2": "test_2", "answer3": "test_3", "answer4": "test_4",
                        "correct_answer": "4"},
            'question': "Does create test passed?",
            'points': 2
        }
        response = self.client.post('/questions/', self.data, format='json')
        is_passed = response.status_code == status.HTTP_201_CREATED

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Creating question with answers"
        })

    def test_get_question(self):
        response = self.client.get(reverse('questionviewset-detail', args=[self.question.id]), format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        is_passed = response.status_code == status.HTTP_200_OK

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Get one question"
        })

    def test_update_question(self):
        self.data = {
            'answers': {"answer1": "updated_test_1", "answer2": "updated_test_2", "answer3": "updated_test_3", "answer4": "test_4",
                        "correct_answer": "4"},
            'question': "Does update of record work?",
            'points': 3
        }

        response = self.client.put(reverse('questionviewset-detail', args=[self.question.id]), self.data, format='json')
        is_passed = response.status_code == status.HTTP_200_OK
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Update question"
        })

    def test_delete_question(self):
        response = self.client.delete(reverse('questionviewset-detail', args=[self.question.id]), format='json')
        is_passed = response.status_code == status.HTTP_204_NO_CONTENT
        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Delete question"
        })

    @classmethod
    def tearDownClass(cls):
        send_test_csv_report(test_results=TEST_RESULTS)

