from django.urls import path
from .views import NextQuestionView, AnswerQuestionView

urlpatterns = [
    path('next/', NextQuestionView.as_view(), name='next-question'),
    path('answer/', AnswerQuestionView.as_view(), name='answer-question'),
]
