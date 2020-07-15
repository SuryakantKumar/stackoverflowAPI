from django.urls import path
from . import views

urlpatterns = [
    path('questions', views.QuestionListCreateView.as_view()),
    path('questions/<int:pk>', views.QuestionRetrieveUpdateDeleteView.as_view(),
         name='question-detail'),
    path('questions/<int:pk>/answers', views.AnswerListCreateView.as_view())
]
