"""
api/tests.py

Test suite for API-level logic, ensuring endpoints deliver expected results,
pagination, and filtering.
Integrates with models from 'questions', 'answers', and 'tags'.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from questions.models import Question
from tags.models import Tag

User = get_user_model()

class QuestionSearchApiTest(TestCase):
	"""
	Test API search, filtering, and pagination for the questions endpoint.
	"""

	def setUp(self):
		"""
		Create test users, tags, and questions for API tests.
		"""
		self.client = APIClient()
		self.user = User.objects.create_user(username='testuser', password='pass')
		self.tag1 = Tag.objects.create(name='DjangoT')
		self.tag2 = Tag.objects.create(name='PythonT')
		# Create 8 questions: 5 with tag1, 3 with tag2
		for i in range(5):
			q = Question.objects.create(
				title=f'Django q{i}',
				body='Django question body.',
				author=self.user,
			)
			q.tags.add(self.tag1)
		for i in range(3):
			q = Question.objects.create(
				title=f'Python q{i}',
				body='Python question body.',
				author=self.user,
			)
			q.tags.add(self.tag2)

	def test_search_by_title(self):
		"""
		Search returns expected questions for title matches.
		"""
		url = reverse('question-search-api')
		resp = self.client.get(url, {'search': 'Python'})
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		self.assertGreaterEqual(data['count'], 3)
		for q in data['results']:
			self.assertIn('Python', q['title'])

	def test_filter_by_tag(self):
		"""
		Filtering by tag returns only matching questions.
		"""
		url = reverse('question-search-api')
		resp = self.client.get(url, {'tag': self.tag1.id})
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		# Should get all questions tagged Django (5)
		self.assertGreaterEqual(data['count'], 5)
		for q in data['results']:
			tag_names = [t['name'] for t in q['tags']]
			self.assertIn('DjangoT', tag_names)

	def test_pagination(self):
		"""
		The API paginates results correctly.
		"""
		url = reverse('question-search-api')
		resp1 = self.client.get(url, {'page': 1, 'page_size': 3})
		resp2 = self.client.get(url, {'page': 2, 'page_size': 3})
		data1 = resp1.json()
		data2 = resp2.json()
		self.assertEqual(resp1.status_code, 200)
		self.assertEqual(resp2.status_code, 200)
		self.assertEqual(len(data1['results']), 3)
		self.assertEqual(data1['page_size'], 3)
		# There should be different questions on different pages
		ids_page1 = set(q['id'] for q in data1['results'])
		ids_page2 = set(q['id'] for q in data2['results'])
		self.assertTrue(ids_page1.isdisjoint(ids_page2))

	def test_search_and_tag_filter_combined(self):
		"""
		Searching and filtering by tag at the same time works as expected.
		"""
		url = reverse('question-search-api')
		resp = self.client.get(url, {'tag': self.tag1.id, 'search': 'Django'})
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		for q in data['results']:
			tag_names = [t['name'] for t in q['tags']]
			self.assertIn('DjangoT', tag_names)
			self.assertIn('Django', q['title'])

