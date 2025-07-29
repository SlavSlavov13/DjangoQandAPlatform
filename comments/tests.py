"""
comments/tests.py

Test suite for the Comment model, including generic relation functionality.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from questions.models import Question
from answers.models import Answer
from comments.models import Comment

User = get_user_model()

class CommentModelTest(TestCase):
	"""
	Tests for Comment fields and generic relation to Question/Answer.
	"""
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='xpass')
		self.q = Question.objects.create(title='Q Title', body='Q Body', author=self.user)
		self.a = Answer.objects.create(question=self.q, author=self.user, content='Answer Content')

	def test_comment_on_question(self):
		comment = Comment.objects.create(
			author=self.user,
			content='Comment on question',
			content_type=ContentType.objects.get_for_model(Question),
			object_id=self.q.pk
		)
		self.assertEqual(comment.content_object, self.q)
		self.assertIn('on', str(comment))

	def test_comment_on_answer(self):
		comment = Comment.objects.create(
			author=self.user,
			content='Comment on answer',
			content_type=ContentType.objects.get_for_model(Answer),
			object_id=self.a.pk
		)
		self.assertEqual(comment.content_object, self.a)

	def test_invalid_content_type(self):
		from django.contrib.auth import get_user_model
		ct_user = ContentType.objects.get_for_model(User)
		comment = Comment(
			author=self.user,
			content='Bad comment',
			content_type=ct_user,
			object_id=self.user.pk
		)
		with self.assertRaises(Exception):
			comment.clean()

	def test_str(self):
		comment = Comment.objects.create(
			author=self.user,
			content="Nice one!",
			content_type=ContentType.objects.get_for_model(Question),
			object_id=self.q.pk
		)
		self.assertIn("Comment by", str(comment))
