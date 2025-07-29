"""
comments/urls.py

Routing for adding, editing, and deleting comments for questions and answers.
Provides separate endpoints for each action and parent object type.
"""

from django.urls import path, include
from .views import AddCommentView, EditCommentView, CommentDeleteView

urlpatterns = [
	path('question-<int:question_id>/', include([
		path('add/', AddCommentView.as_view(), name='add-comment-to-question'),
		path('comment-<int:comment_id>/', include([
			path('edit/', EditCommentView.as_view(), name='edit-comment-to-question'),
			path('delete/', CommentDeleteView.as_view(), name='delete-comment-to-question'),
		]))

	])),
	path('answer-<int:answer_id>/', include([
		path('add/', AddCommentView.as_view(), name='add-comment-to-answer'),
		path('comment-<int:comment_id>/', include([
			path('edit/', EditCommentView.as_view(), name='edit-comment-to-answer'),
			path('delete/', CommentDeleteView.as_view(), name='delete-comment-to-answer'),
		]))
	])),
	]
