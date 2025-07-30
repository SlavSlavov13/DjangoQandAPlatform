"""
answers/models.py

Defines the Answer model for associating user answers with questions,
supporting user-contributed Q&A and related comments in a Django application.
"""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import Truncator

UserModel = get_user_model()

class Answer(models.Model):
	"""
	Represents an answer posted by a user to a specific question.

	- Linked to a Question (foreign key, required).
	- Linked to an Author (User, required).
	- Supports generic related comments (one-to-many, via Django's contenttypes).
	"""

	question = models.ForeignKey(
		to='questions.Question',
		on_delete=models.CASCADE,
		related_name='answers',
		help_text="The question to which this answer belongs."
	)
	author = models.ForeignKey(
		UserModel,
		on_delete=models.CASCADE,
		help_text="The user who authored this answer."
	)
	content = models.TextField(
		help_text="Main body of the answer."
	)
	created_at = models.DateTimeField(
		auto_now_add=True,
		help_text="Timestamp when the answer was created."
	)
	comments = GenericRelation(
		to='comments.Comment',
		related_query_name='answer',
		help_text="All comments associated with this answer."
	)

	def __str__(self):
		"""
		String representation for admin, debug, and logging.
		Example: 'Answer by johndoe on How to test models?'
		"""
		question_title = Truncator(str(self.question)).chars(50)
		return f'Answer by {self.author.username} on {question_title}'

