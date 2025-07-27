from django.urls import path
from .views import AddCommentView

urlpatterns = [
	path('add/question-<int:question_id>/', AddCommentView.as_view(), name='add_comment_to_question'),
	path('add/answer-<int:answer_id>/', AddCommentView.as_view(), name='add_comment_to_answer'),
]
