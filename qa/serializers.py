from rest_framework import serializers
from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.HyperlinkedRelatedField(
        lookup_field='pk',
        view_name='question-detail',
        read_only=True
    )

    class Meta:
        model = Answer
        fields = ('user', 'question', 'content', 'votes')


class AnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('user', 'question', 'content', 'votes')


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'title', 'description', 'answers')
