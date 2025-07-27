from rest_framework import generics, filters
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from questions.models import Question
from .serializers import QuestionSerializer

class QuestionSearchAPIView(generics.ListAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	filter_backends = [filters.SearchFilter, DjangoFilterBackend]
	search_fields = ['title', 'body']
	filterset_fields = ['tags__id']  # Enables filtering by tag ID through query parameter `tags__id`

	def get_queryset(self):
		queryset = super().get_queryset()
		tag_ids = self.request.query_params.getlist('tag')  # getlist for multiple values
		if tag_ids:
			queryset = queryset.filter(tags__id__in=tag_ids).distinct()
		return queryset

