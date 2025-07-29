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

	def test_manual_slug_is_preserved(self):
		"""
		If a slug is supplied explicitly, it is not overwritten on save.
		"""
		tag = Tag(name="Django", slug="custom-slug")
		tag.save()
		self.assertEqual(tag.slug, "custom-slug")


class TagAdminTests(TestCase):
	"""
	Tests customized TagAdmin behavior regarding the 'slug' field's
	read-only status depending on user group membership.
	"""

	def setUp(self):
		# Ensure the "Staff Moderators" group is only created if not present
		self.mod_group, _ = Group.objects.get_or_create(name="Staff Moderators")

		# Regular staff/superuser, not a moderator
		self.staff = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

		# This user is a "moderator"
		self.moderator = User.objects.create_user('mod', 'mod@example.com', 'pass')
		self.moderator.groups.add(self.mod_group)
		self.moderator.save()

		self.factory = RequestFactory()

	def test_slug_readonly_for_moderators(self):
		"""
		If user is in 'Staff Moderators', slug is readonly in the admin.
		"""
		from .admin import TagAdmin

		admin_instance = TagAdmin(Tag, admin.site)
		request = self.factory.get('/')
		request.user = self.moderator

		readonly = admin_instance.get_readonly_fields(request, None)
		self.assertIn('slug', readonly)

	def test_slug_editable_for_non_moderators(self):
		"""
		If user is NOT in 'Staff Moderators', slug is editable in the admin.
		"""
		from .admin import TagAdmin

		admin_instance = TagAdmin(Tag, admin.site)
		request = self.factory.get('/')
		request.user = self.staff

		readonly = admin_instance.get_readonly_fields(request, None)
		self.assertNotIn('slug', readonly)
