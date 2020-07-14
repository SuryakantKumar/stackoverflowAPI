import os
import json

from django.test import Client
from django.conf import settings

from test_plus.test import TestCase
from qa.models import Question, Answer
import random
random.seed(2)


class QuestionListGetTest(TestCase):
    def setUp(self):
        u1 = self.make_user('u1')
        u2 = self.make_user('u2')
        u3 = self.make_user('u3')
        users = [u1, u2, u3]
        self.client = Client()
        for i in range(12):
            user = u1 if i % 2 == 0 else u2
            question = Question.objects.create(
                title=f'question-{i}',
                description=f'question-{i}',
                user=user
            )
            tags = random.choice([['t1', 't2'], ['t3', 't4']])
            for t in tags:
                question.tags.add(t)
            for i in range(3):
                Answer.objects.create(
                    user=users[i],
                    question=question,
                    content=f'answer-{i}',
                    votes=i
                )

    def test_list_get(self):
        page1 = self.client.get('/questions')
        page2 = self.client.get('/questions?page=2')
        page3 = self.client.get('/questions?page=3')
        page4 = self.client.get('/questions?page=4')
        for page in [page1, page2, page3]:
            self.assertEqual(page1.status_code, 200)
        self.assertEqual(page4.status_code, 404)

        pages = [page1, page2, page3]
        MOCK_DATA_DIR = os.path.join(settings.BASE_DIR, 'mock_data')
        for i, page in zip(range(1, 4), pages):
            with open(f'{MOCK_DATA_DIR}/questions_page_{i}.json', 'r') as f:
                content = f.read()
        expected_output = json.loads(content)
        self.assertEqual(page.json(), expected_output)


class QuestionPostTest(TestCase):
    def setUp(self):
        self.user = self.make_user('u1')
        self.client = Client()
        self.client.login(username="u1", password="password")

    def test_question_create(self):
        data = {
            'title': 'q1',
            'description': 'hello'
        }
        response = self.client.post(
            '/questions',
            json.dumps(data),
            content_type='application/json'
        )
        expected_output = {
            'id': 1,
            'title': 'q1',
            'description': 'hello',
            'answers': []
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), expected_output)
        question = Question.objects.get(pk=1)
        self.assertEqual(question.id, 1)
        self.assertEqual(question.title, 'q1')
        self.assertEqual(question.description, 'hello')


class QuestionDetailTest(TestCase):
    def setUp(self):
        self.user1 = self.make_user('u1')
        self.client1 = Client()
        self.client1.login(username="u1", password="password")

        self.user2 = self.make_user('u2')
        self.client2 = Client()
        self.client2.login(username='u2', password='password')

        self.question = Question.objects.create(
            user=self.user1,
            title='q1',
            description='hello'
        )

    def test_question_get(self):
        response = self.client1.get('/questions/1')
        expected_output = {
            'id': 1,
            'title': 'q1',
            'description': 'hello',
            'answers': []
        }
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_output)

    def test_question_get_not_found(self):
        response = self.client1.get('/questions/100')
        self.assertEqual(response.status_code, 404)

    def test_question_update(self):
        data = {
            'title': 'q1',
            'description': 'modified q1'
        }
        data = json.dumps(data)
        response = self.client1.put(
            '/questions/1',
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        modified_question = Question.objects.get(id=self.question.id)
        self.assertEqual(modified_question.title, 'q1')
        self.assertEqual(modified_question.description, 'modified q1')
        self.assertEqual(Question.objects.count(), 1)

    def test_question_update_forbidden(self):
        data = {
            'title': 'q1',
            'description': 'modified q1'
        }
        data = json.dumps(data)
        response = self.client2.put(
            '/questions/1',
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)
        question = Question.objects.get(id=self.question.id)
        self.assertEqual(question.title, 'q1')
        self.assertEqual(question.description, 'hello')
        self.assertEqual(Question.objects.count(), 1)
