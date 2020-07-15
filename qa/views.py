# from django.shortcuts import render
# from django.http.response import JsonResponse
# from rest_framework.parsers import JSONParser
# # from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer, AnswerDetailSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class QuestionListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# @api_view(['GET', 'POST'])
# def questions_list(request):
#     if request.method == 'GET':
#         questions = Question.objects.all()
#         questions_serializer = QuestionSerializer(questions, many=True)
#         return JsonResponse(questions_serializer.data, safe=False)

#     elif request.method == 'POST':
#         questions_data = JSONParser().parse(request)
#         questions_serializer = QuestionSerializer(data=questions_data)
#         if questions_serializer.is_valid():
#             questions_serializer.save()
#             return JsonResponse(questions_serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(questions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# @api_view(['GET', 'PUT', 'DELETE'])
# def questions_detail(request, pk):
#     try:
#         questions = Question.objects.get(pk=pk)
#     except Question.DoesNotExist:
#         return JsonResponse({'message': 'The Question does not exist'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         questions_serializer = QuestionSerializer(questions)

#         return JsonResponse(questions_serializer.data)

#     elif request.method == 'PUT':
#         questions_data = JSONParser().parse(request)
#         questions_serializer = QuestionSerializer(
#             questions, data=questions_data)
#         if questions_serializer.is_valid():
#             questions_serializer.save()
#             return JsonResponse(questions_serializer.data)
#         return JsonResponse(questions_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         questions.delete()
#         return JsonResponse({'message': 'Question was deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class AnswerListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = AnswerSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Answer.objects.filter(question=pk)


# @api_view(['GET', 'POST'])
# def answers_list(request, pk):
#     if request.method == 'GET':
#         answers = Answer.objects.filter(question__pk=pk)

#         answers_serializer = AnswerSerializer(answers, many=True)
#         return JsonResponse(answers_serializer.data, safe=False)

#     elif request.method == 'POST':
#         answers_data = JSONParser().parse(request)
#         answers_serializer = AnswerSerializer(data=answers_data)

#         if answers_serializer.is_valid():
#             answers_serializer.save()
#             return JsonResponse(answers_serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(answers_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
