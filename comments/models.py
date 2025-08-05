"""
comments/models.py

Defines Comment model for associating user comments
with questions, answers, or other comments using Django's generic relations.
"""
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType

from DjangoQandAPlatform.validators import SizeValidator

UserModel = get_user_model()

class Comment(models.Model):
	"""
	Represents a user comment, linked generically to either a Question,
	Answer, or another Comment (for nested commenting).
	"""
	author = models.ForeignKey(
		to=UserModel,
		on_delete=models.CASCADE,
		help_text="User who authored the comment."
	)
	content = models.TextField(
		help_text="Text content of the comment."
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		help_text="Timestamp when the comment was created."
	)
	content_type = models.ForeignKey(
		to=ContentType,
		on_delete=models.CASCADE,
		limit_choices_to=(
				models.Q(app_label='questions', model='question') |
				models.Q(app_label='answers', model='answer') |
				models.Q(app_label='comments', model='comment')  # Allow commenting on comments
		),
		help_text="Type: Question, Answer, or Comment referenced."
	)
	object_id = models.PositiveIntegerField(
		help_text="ID of the related Question, Answer, or Comment."
	)
	content_object = GenericForeignKey('content_type', 'object_id')

	# Optional reverse relation to get child comments of this comment
	comments = GenericRelation('self', content_type_field='content_type', object_id_field='object_id')

	media = models.ImageField(
		blank=True, null=True,
		validators=[SizeValidator(10)],
		help_text="Optional image for context.",
	)


	def clean(self):
		"""
		Restrict comments to only refer to questions, answers, or comments.
		"""
		allowed_models = ['question', 'answer', 'comment']
		if self.content_type.model not in allowed_models:
			raise ValidationError('Comments may only refer to Question, Answer or Comment objects.')

	def __str__(self):
		"""
		Reader-friendly string representation for lists and admin display.
		"""
		return f"Comment by {self.author} on {self.content_object}"
