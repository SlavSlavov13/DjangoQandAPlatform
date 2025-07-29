"""
questions/tests.py

Unit and integration test suite for Question model logic and relationships.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from questions.models import Question
from tags.models import Tag

User = get_user_model()

class QuestionModelTest(TestCase):
	"""
	Tests for correct field assignment, string representation, and tag associations.
	"""

	def setUp(self):
		self.user = User.objects.create_user(username='examiner', password='1234')
		self.tag1 = Tag.objects.create(name="Django")
		self.tag2 = Tag.objects.create(name="Python")

	def test_create_question(self):
		question = Question.objects.create(
			title="How to write Django admin comments?",
			body="What is the best practice?",
			author=self.user
		)
		self.assertEqual(question.author.username, 'examiner')
		self.assertEqual(str(question), question.title)
		self.assertIsNotNone(question.created_at)
		self.assertIsNotNone(question.updated_at)

	def test_tags_assignment(self):
		q = Question.objects.create(
			title="How to tag Qs?",
			body="Test body.",
			author=self.user
		)
		q.tags.add(self.tag1, self.tag2)
		self.assertIn(self.tag1, q.tags.all())
		self.assertIn(self.tag2, q.tags.all())
		self.assertEqual(q.tags.count(), 2)
		# Tags should link back to question
		self.assertIn(q, self.tag1.questions.all())
