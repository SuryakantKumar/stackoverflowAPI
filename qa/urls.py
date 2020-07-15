from django.urls import path
from . import views

urlpatterns = [
    path('questions', views.questions_list),
    path('questions/<int:pk>', views.questions_detail)
]
