from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
	name = models.CharField(max_length=30, unique=True)
	slug = models.SlugField(max_length=40, unique=True, blank=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name