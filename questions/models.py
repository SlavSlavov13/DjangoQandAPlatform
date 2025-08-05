"""
questions/models.py

Question model for user Q&A, with tags, author, and generic comments.
"""
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import Truncator

from DjangoQandAPlatform.validators import SizeValidator

UserModel = get_user_model()

class Question(models.Model):
	"""
	Represents a posted question.
	Includes generic relation for comments and a set of tags.
	"""
	title = models.CharField(max_length=150, help_text="Question headline.")
	body = models.TextField(help_text="Detailed question description.")
	author = models.ForeignKey(
		to=UserModel,
		on_delete=models.CASCADE,
		help_text="User who asked the question."
	)
	tags = models.ManyToManyField(
		to='tags.Tag',
		blank=True,
		related_name='questions',
		help_text="Tags for topic categorization."
	)
	created_at = models.DateTimeField(auto_now_add=True, help_text="Creation timestamp.")
	updated_at = models.DateTimeField(auto_now=True, help_text="Update timestamp.")
	comments = GenericRelation(
		to='comments.Comment',
		related_query_name='question',
		help_text="Comments associated with this question."
	)
	media = models.ImageField(
		blank=True, null=True,
		validators=[SizeValidator(10)],
		help_text="Optional image for context.",
	)

	def __str__(self):
		"""Return the question's title."""
		return Truncator(str(self.title)).chars(50)


	class Meta:
		ordering = ['-created_at']
