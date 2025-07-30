"""
Models for the Tagging system.

Defines the Tag model, which supports slugs for clean URLs and uniqueness.
"""

from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
	"""
	Represents a tag that can be associated with questions, posts, etc.

	Attributes:
		name: The display name of the tag. Must be unique.
		slug: A URL-friendly, unique version of the tag name (auto-generated).
	"""
	name = models.CharField(max_length=30, unique=True,
	                        help_text="Unique human-readable tag name (e.g. 'python').")
	slug = models.SlugField(max_length=40, unique=True, blank=True,
	                        help_text="Always auto-generated from name")

	def save(self, *args, **kwargs):
		"""
		Automatically set or update slug to a slugified version
		of the current name, always.
		"""
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		"""String representation: just the tag name."""
		return self.name
