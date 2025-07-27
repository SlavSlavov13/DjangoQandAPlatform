from rest_framework import generics, filters
from questions.models import Question
from .serializers import QuestionSerializer

class QuestionSearchAPIView(generics.ListAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'body']
