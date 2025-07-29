from django.db import models
from django.utils.text import slugify


class Badge(models.Model):
	name = models.CharField(max_length=50, unique=True, help_text="Unique badge name, e.g., 'Top Answerer'")
	description = models.TextField(help_text="What this badge is awarded for")
	icon = models.ImageField(upload_to='badges/', blank=True, null=True, help_text="Optional badge icon image")
	slug = models.SlugField(max_length=40, unique=True, blank=True)

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)
