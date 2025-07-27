from django.urls import path
from .views import (
	QuestionListView,
	QuestionCreateView,
	QuestionUpdateView,
	QuestionDeleteView, QuestionDetailView,
)

urlpatterns = [
	path("", QuestionListView.as_view(), name="questions_list"),
	path("create/", QuestionCreateView.as_view(), name="question_create"),
	path("<int:pk>/update/", QuestionUpdateView.as_view(), name="question_update"),
	path("<int:pk>/details/", QuestionDetailView.as_view(), name="question_details"),
	path("<int:pk>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
]
