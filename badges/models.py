"""
badges/models.py

Defines the Badge model representing user achievement badges
with image, auto-generated slug, and unique naming.
"""

from django.db import models
from django.utils.text import slugify

class Badge(models.Model):
	"""
	Represents a unique achievement badge for rewarding user activity.
	- Each badge has a name, description, optional icon, and slug.
	- Slug is auto-populated from name if not provided.
	"""
	name = models.CharField(
		max_length=50,
		unique=True,
		help_text="Unique badge name, e.g., 'Top Answerer'"
	)
	description = models.TextField(
		help_text="What this badge is awarded for"
	)
	icon = models.ImageField(
		upload_to='badges/',
		blank=True, null=True,
		help_text="Optional badge icon image"
	)
	slug = models.SlugField(
		max_length=40,
		unique=True,
		blank=True,
		help_text="Always auto-generated from name"
	)

	def __str__(self):
		"""String for admin and debug: badge name."""
		return self.name

	def save(self, *args, **kwargs):
		"""
		Automatically set or update slug to a slugified version
		of the current name, always.
		"""
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)
