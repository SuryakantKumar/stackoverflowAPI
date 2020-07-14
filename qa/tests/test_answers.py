import os
import json

from django.test import Client
from django.conf import settings

from test_plus.test import TestCase
from qa.models import Question, Answer
import random
random.seed(2)


class AnswerListGetTest(TestCase):
    def setUp(self):
        u1 = self.make_user('u1')
        u2 = self.make_user('u2')
        u3 = self.make_user('u3')
        users = [u1, u2, u3]

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

    def test_answer_list_get(self):
        client = Client()
        client.login(username='u1', password='password')

        response = client.get('/questions/1/answers')
        self.assertEqual(response.status_code, 200)
        MOCK_DATA_DIR = os.path.join(settings.BASE_DIR, 'mock_data')
        with open(f'{MOCK_DATA_DIR}/answer_list.json', 'r') as f:
            expected_content = f.read()
        expected_content = json.loads(expected_content)
        self.assertEqual(response.json(), expected_content)

