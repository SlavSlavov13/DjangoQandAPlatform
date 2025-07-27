from rest_framework import serializers
from questions.models import Question
from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ['name']
		read_only_fields = fields

class QuestionSerializer(serializers.ModelSerializer):
	author_pk = serializers.PrimaryKeyRelatedField(source='author', read_only=True)
	tags = TagSerializer(many=True, read_only=True)
	class Meta:
		model = Question
		fields = ['id', 'title', 'body', 'tags', 'created_at', 'author_pk']
		read_only_fields = fields
