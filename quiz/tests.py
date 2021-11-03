import inspect
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from .serializers import *
from .utils import send_test_csv_report

# Create your tests here.

TEST_RESULTS = []
TEST_DIR = 'test_data'


# QUESTION TESTS
class QuestionTestCase(APITestCase):
    def setUp(self) -> None:
        self.answer = Answer.objects.create(id=1, answer1="test_1", answer2="test_2", answer3="test_3",
                                            answer4="test_4", correct_answer="1")
        self.question = Question.objects.create(id=1, answers_id=1, question="Does test passed?", points=3, category=None)
        self.client = APIClient()

    def test_create_question(self):
        self.data = {
            'id': 2,
            'answers': {"answer1": "test_1", "answer2": "test_2", "answer3": "test_3", "answer4": "test_4",
                        "correct_answer": "4"},
            'question': "Does create test passed?",
            'points': 2,
            'category': None
        }
        response = self.client.post(reverse('questions-list'), self.data, format='json')
        is_passed = response.status_code == status.HTTP_201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assert

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Creating question with answers"
        })

    def test_get_question(self):
        response = self.client.get(reverse('questions-detail', args=[self.question.id]), format='json')
        is_passed = response.status_code == status.HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Get one question"
        })

    def test_update_question(self):
        self.data = {
            'answers': {"answer1": "updated_test_1", "answer2": "updated_test_2", "answer3": "updated_test_3",
                        "answer4": "test_4",
                        "correct_answer": "4"},
            'question': "Does update of record work?",
            'points': 3
        }

        response = self.client.put(reverse('questions-detail', args=[self.question.id]), self.data, format='json')
        is_passed = response.status_code == status.HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Update question"
        })

    def test_delete_question(self):
        response = self.client.delete(reverse('questions-detail', args=[self.question.id]), format='json')
        is_passed = response.status_code == status.HTTP_204_NO_CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Delete question"
        })

    @classmethod
    def tearDownClass(cls):
        send_test_csv_report(test_results=TEST_RESULTS)


# CATEGORY TESTS
class CategoryTestCase(APITestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(id=1, name='Test1', image=None, slug="test1", color="#FFFFFF",
                                                description="Lorem ipsum")
        self.client = APIClient()

    def test_create_category(self):
        self.data = {
            'id': 3,
            'name': 'test_category_name',
            'image': None,
            'category_url': 'test-category-name',
            'color': '#AABBCC',
            'description': "Lorem ipsum",
        }

        response = self.client.post(reverse('categories-list'), self.data, format='json')
        is_passed = response.status_code == status.HTTP_201_CREATED
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Creating category"
        })

    def test_get_category(self):
        response = self.client.get(reverse('categories-detail', args=[self.category.name]), format='json')
        is_passed = response.status_code == status.HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Get category"
        })

    def test_update_category(self):
        self.data = {'name': 'Updated_category_name', 'image': None, 'category_url': 'Updated_slug_name',
                     'color': '#FF00A5',
                     'description': 'No description'}
        response = self.client.put(reverse('categories-detail', args=[self.category.name]), self.data, format='json')
        is_passed = response.status_code == status.HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Update category"
        })

    def test_delete_category(self):
        response = self.client.delete(reverse('categories-detail', args=[self.category.name]), format='json')
        is_passed = response.status_code == status.HTTP_204_NO_CONTENT
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        TEST_RESULTS.append({
            "test_name": "Passed" if is_passed else "Failed",
            "result": inspect.currentframe().f_code.co_name,
            "test_description": "Delete category"
        })

    @classmethod
    def tearDownClass(cls):
        send_test_csv_report(test_results=TEST_RESULTS)


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        pass

# Not needed...
# class QuizTestCase(APITestCase):
#     def setUp(self) -> None:
#         self.answer1 = Answer.objects.create(id=1, answer1="test_1", answer2="test_2", answer3="test_3",
#                                              answer4="test_4", correct_answer="1")
#         self.question1 = Question.objects.create(id=2, answers_id=1, question="Wazzup?", points=3)
#
#         self.answer2 = Answer.objects.create(id=2, answer1="test_1", answer2="test_2", answer3="test_3",
#                                              answer4="test_4", correct_answer="1")
#         self.question2 = Question.objects.create(id=3, answers_id=2, question="WAZZZZZZZUPPPP", points=3)
#         self.category = Category.objects.create(id=1, name='Test_category', image=None, slug="test-category", color="#FFFFFF",
#                                                 description="Lorem ipsum")
#         self.quiz = Quiz.objects.create(id=1, category_id='Test_category')
#         self.quiz.question.add(self.question1, self.question2)
