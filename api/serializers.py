"""
api/serializers.py

Serializers for converting Question and Tag models to and from JSON
for use in REST API endpoints.
"""

from rest_framework import serializers
from questions.models import Question
from tags.models import Tag

class TagSerializer(serializers.ModelSerializer):
	"""
	Serializer for the Tag model.
	Used to represent tags attached to questions as simple JSON objects.
	"""
	class Meta:
		model = Tag
		fields = ['name']
		read_only_fields = fields

class QuestionSerializer(serializers.ModelSerializer):
	"""
	Serializer for the Question model (with related tags and author).
	Exposes all fields required for client-side search/list/detail use.
	"""
	author_pk = serializers.PrimaryKeyRelatedField(source='author', read_only=True)
	tags = TagSerializer(many=True, read_only=True)

	class Meta:
		model = Question
		fields = ['id', 'title', 'body', 'tags', 'created_at', 'author_pk']
		read_only_fields = fields
