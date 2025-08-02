"""
Models for the users app: UserProfile connects user to bio, avatar, badges.
"""
from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class UserProfile(models.Model):
	"""
	Extends the user model with additional fields for the profile.

	- Links to one user (OneToOneField).
	- Stores bio, avatar image, and badge relationships.
	"""
	user = models.OneToOneField(
		to=UserModel,
		on_delete=models.CASCADE,
		related_name='profile',
		help_text='Related user for this profile.'
	)
	bio = models.TextField(
		blank=True,
		help_text='Write a short bio'
	)
	avatar = models.ImageField(
		blank=True,
		null=True,
		help_text='Profile avatar image (optional)'
	)
	badges = models.ManyToManyField(
		'badges.Badge',
		blank=True,
		related_name='users',
		help_text="Badges awarded to this user"
	)

	def __str__(self):
		"""
		Display as username in Django admin/representation.
		"""
		return f'{self.user.username}'

class InitialSetup(models.Model):
	groups_created = models.BooleanField(default=False)
