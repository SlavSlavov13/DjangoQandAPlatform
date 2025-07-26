from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

UserModel = get_user_model()

class Vote(models.Model):
	user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE, related_name='votes')
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
	value = models.SmallIntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')], help_text="Vote: 1=up, -1=down")
	voted_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'content_type', 'object_id')  # Prevents multiple votes by the same user

	def __str__(self):
		return f'{self.user.user.username} voted {self.value} on {self.content_object}'
