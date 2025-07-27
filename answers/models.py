from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

UserModel = get_user_model()
class Answer(models.Model):
	question = models.ForeignKey(to='questions.Question', on_delete=models.CASCADE, related_name='answers')
	author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	comments = GenericRelation(to='comments.Comment', related_query_name='answer')

def __str__(self):
		return f'Answer by {self.author.username} on {self.question}'