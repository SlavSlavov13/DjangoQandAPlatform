"""
api/views.py

Defines API endpoints for question search and retrieval.
Provides pagination, searching, and tag-based filtering via DRF.
"""

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from questions.models import Question
from .pagination import QuestionApiPagination
from .serializers import QuestionSerializer

class QuestionSearchAPIView(generics.ListAPIView):
	"""
	API endpoint for listing and searching questions.

	Supports:
	- Text search on question title and body via the 'search' query parameter.
	- Filtering by tag(s) using 'tag' query parameter(s).
	- Pagination (with page size set in pagination.py).
	"""
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	filter_backends = [filters.SearchFilter, DjangoFilterBackend]
	search_fields = ['title', 'body']
	filterset_fields = ['tags__id']  # Enables filtering by tag ID via 'tag' param
	pagination_class = QuestionApiPagination

	def get_queryset(self):
		"""
		Optionally filters queryset by tag(s) if tag filters are present in query params.
		Tags can be passed as multiple 'tag' parameters.
		"""
		queryset = super().get_queryset()
		tag_ids = self.request.query_params.getlist('tag')
		if tag_ids:
			queryset = queryset.filter(tags__id__in=tag_ids).distinct()
		return queryset
