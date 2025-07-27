from django.urls import path
from .views import QuestionSearchAPIView

urlpatterns = [
	path('questions/search/', QuestionSearchAPIView.as_view(), name='question_search_api'),
]
