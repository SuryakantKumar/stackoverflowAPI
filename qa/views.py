from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def questions_list(request):
    if request.method == 'GET':
        questions = Question.objects.all()

        questions_serializer = QuestionSerializer(questions, many=True)
        return JsonResponse(questions_serializer.data, safe=False)

    elif request.method == 'POST':
        questions_data = JSONParser().parse(request)
        questions_serializer = QuestionSerializer(data=questions_data)

        if questions_serializer.is_valid():
            questions_serializer.save()
            return JsonResponse(questions_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(questions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def questions_detail(request, pk):
    try:
        questions = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return JsonResponse({'message': 'The Question does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        questions_serializer = QuestionSerializer(questions)

        return JsonResponse(questions_serializer.data)

    elif request.method == 'PUT':
        questions_data = JSONParser().parse(request)
        questions_serializer = QuestionSerializer(
            questions, data=questions_data)
        if questions_serializer.is_valid():
            questions_serializer.save()
            return JsonResponse(questions_serializer.data)
        return JsonResponse(questions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        questions.delete()
        return JsonResponse({'message': 'Question was deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
