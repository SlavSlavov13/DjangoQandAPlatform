from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import models


UserModel = get_user_model()

class UserProfile(models.Model):
	user = models.OneToOneField(to=UserModel, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(blank=True, help_text='Write a short bio')
	avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
	badges = models.ManyToManyField(
		'badges.Badge',
		blank=True,
		related_name='users',
		help_text="Badges awarded to this user"
	)

	def __str__(self):
		return f'{self.user.username}'
