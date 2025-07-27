from django.urls import path

from answers.views import AnswerCreateView

urlpatterns = [
	path('answer-question/<int:question_id>/', AnswerCreateView.as_view(), name='create-answer')
]