"""
api/urls.py

Defines URLs for the API endpoints provided by this app.
"""

from django.urls import path
from .views import QuestionSearchAPIView

urlpatterns = [
	# Endpoint to search and filter questions
	path('questions/search/', QuestionSearchAPIView.as_view(), name='question_search_api'),
]
