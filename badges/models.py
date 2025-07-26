from django.db import models

class Badge(models.Model):
	name = models.CharField(max_length=50, unique=True, help_text="Unique badge name, e.g., 'Top Answerer'")
	description = models.TextField(help_text="What this badge is awarded for")
	icon = models.ImageField(upload_to='badges/', blank=True, null=True, help_text="Optional badge icon image")

	def __str__(self):
		return self.name
