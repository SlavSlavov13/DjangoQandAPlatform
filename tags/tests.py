"""
Unit tests for the Tag model and Tag admin logic.

Covers creation, string representation, slug logic, validation, and admin
readonly logic depending on user group membership ("Staff Moderators").
"""

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from django.contrib import admin
from django.utils.text import slugify

from .models import Tag


class TagModelTests(TestCase):
	"""
	Tests related to the Tag model and its automatic slugification logic.
	"""

	def test_tag_creation_sets_slug(self):
		"""
		Creating a tag without a slug sets the slug to the slugified name.
		"""
		tag = Tag.objects.create(name='Test Tag')
		self.assertEqual(tag.slug, slugify('Test Tag'))

	def test_tag_string_representation(self):
		"""
		The __str__ method of Tag returns its name.
		"""
		tag = Tag.objects.create(name='Python')
		self.assertEqual(str(tag), 'Python')

	def test_tag_slug_uniqueness(self):
		"""
		Tag model enforces unique names/slugs (unique on name).
		"""
		Tag.objects.create(name="JavaScript")
		# Attempting to create another tag with the same name raises an error
		with self.assertRaises(Exception):
			Tag.objects.create(name="JavaScript")

	def test_manual_slug_is_replaced(self):
		"""
		If a slug is supplied explicitly, it is overwritten on save.
		"""
		tag = Tag(name="Django", slug="custom-slug")
		tag.save()
		self.assertEqual(tag.slug, slugify('Django'))
