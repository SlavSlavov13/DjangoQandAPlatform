from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class Question(models.Model):
	title = models.CharField(max_length=150)
	body = models.TextField()
	author = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
	tags = models.ManyToManyField(to='tags.Tag', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title