"""
answers/tests.py

Test suite for the Answer model, covering unit-level model behavior
as well as integration with related Question and User instances.

Uses Django's TestCase for database-backed checks.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from questions.models import Question
from answers.models import Answer
from comments.models import Comment

User = get_user_model()

class AnswerModelUnitTest(TestCase):
	"""
	Unit tests for the Answer model fields and methods.
	"""

	def setUp(self):
		# Create minimal user and question fixtures.
		self.user = User.objects.create_user(username='johndoe', password='secret123')
		self.question = Question.objects.create(
			title="Sample Question",
			body="What is the answer to this sample question?",
			author=self.user
		)

	def test_answer_string_representation(self):
		"""
		__str__ returns expected format.
		"""
		answer = Answer.objects.create(
			question=self.question,
			author=self.user,
			content="This is my answer."
		)
		self.assertIn(self.user.username, str(answer))
		self.assertIn(str(self.question), str(answer))

	def test_answer_fields(self):
		"""
		Checks that all fields are present and accepted.
		"""
		answer = Answer.objects.create(
			question=self.question,
			author=self.user,
			content="Another example answer."
		)
		self.assertEqual(answer.question, self.question)
		self.assertEqual(answer.author, self.user)
		self.assertIsInstance(answer.created_at, type(answer.created_at))  # Should be datetime
		self.assertEqual(answer.comments.count(), 0)

class AnswerIntegrationTest(TestCase):
	"""
	Integration tests: answer with questions, users, and comments.
	"""

	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='secret', email='email1')
		self.other = User.objects.create_user(username='otheruser', password='pass', email='email2')
		self.question = Question.objects.create(
			title="Integration Test Q",
			body="Integration body content.",
			author=self.user,
		)
		self.answer = Answer.objects.create(
			question=self.question,
			author=self.other,
			content="This is an integration test answer."
		)

	def test_answer_links_to_question_and_author(self):
		"""
		The answer is correctly related to both author and question.
		"""
		self.assertEqual(self.answer.question, self.question)
		self.assertEqual(self.answer.author, self.other)

	def test_add_and_query_comments_on_answer(self):
		"""
		Can add and retrieve comments associated via GenericRelation.
		"""
		comment = Comment.objects.create(
			content="Insightful comment.",
			author=self.user,
			content_object=self.answer  # GenericForeignKey to this answer
		)
		# Comments accessible from answer
		self.assertIn(comment, self.answer.comments.all())
		# Also accessible from Comment's related_query_name "answer"
		self.assertIn(self.answer, Answer.objects.filter(comments__pk=comment.pk))

	def test_question_related_answers(self):
		"""
		Can retrieve answers from question.answer_set or question.answers related_name.
		"""
		self.assertIn(self.answer, self.question.answers.all())
		self.assertEqual(self.question.answers.count(), 1)

