from django.urls import path
from . import views
from .views import ApiQuestionListCreateView

urlpatterns = [
    path('questions', ApiQuestionListCreateView.as_view()),
    # path('questions', views.questions_list),
    path('questions/<int:pk>', views.questions_detail),
    path('questions/<int:pk>/answers', views.answers_list)
]
