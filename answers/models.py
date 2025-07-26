from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()
class Answer(models.Model):
	question = models.ForeignKey(to='questions.Question', on_delete=models.CASCADE, related_name='answers')
	author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	is_accepted = models.BooleanField(default=False)

	def __str__(self):
		return f'Answer by {self.author.user.username} on {self.question}'