from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.contenttypes.models import ContentType

UserModel = get_user_model()

class Comment(models.Model):
	author = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	content_type = models.ForeignKey(
		to=ContentType,
		on_delete=models.CASCADE,
		limit_choices_to=(
				models.Q(app_label='questions', model='question') |
				models.Q(app_label='answers', model='answer')
		)
	)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	def clean(self):
		allowed_models = ['question', 'answer']
		if self.content_type.model not in allowed_models:
			raise ValidationError('Comments may only refer to Question or Answer objects.')

	def __str__(self):
		return f"Comment by {self.author} on {self.content_object}"