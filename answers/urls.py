"""
answers/urls.py

URL patterns for answering questions: create, edit, and delete answers.
"""

from django.urls import path, include
from answers.views import AnswerCreateView, AnswerEditView, AnswerDeleteView

urlpatterns = [
	path('answer-question/<int:question_id>/', AnswerCreateView.as_view(), name='create-answer'),
	path('<int:answer_id>/', include([
		path('edit-answer', AnswerEditView.as_view(), name='edit-answer'),
		path('delete-answer', AnswerDeleteView.as_view(), name='delete-answer'),
	]))

]