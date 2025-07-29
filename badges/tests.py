"""
badges/tests.py

Test suite for the Badge model.
Covers creation, slug auto-generation, uniqueness, and optionals.
"""

from django.test import TestCase
from badges.models import Badge

class BadgeModelTest(TestCase):
	"""
	Tests for the Badge model fields and behavior.
	"""

	def test_badge_creation_and_str(self):
		badge = Badge.objects.create(
			name="Test Badge",
			description="Awarded for testing.",
		)
		self.assertEqual(str(badge), "Test Badge")
		self.assertIsInstance(badge.slug, str)

	def test_auto_slug_generation(self):
		badge = Badge.objects.create(
			name="Unique Name Badge",
			description="For uniqueness.",
		)
		expected_slug = "unique-name-badge"
		self.assertEqual(badge.slug, expected_slug)

	def test_slug_uniqueness(self):
		Badge.objects.create(
			name="A",
			description="Desc"
		)
		# Creating a badge with same name should raise integrity error due to unique constraint.
		with self.assertRaises(Exception):
			Badge.objects.create(
				name="A",
				description="Dup"
			)

	def test_badge_icon_optional(self):
		badge = Badge.objects.create(
			name="Iconless",
			description="No icon badge.",
		)
		self.assertFalse(badge.icon)

