"""
Models for the users app: UserProfile connects user to bio, avatar, badges.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.contrib.auth.models import Group as AuthGroup


class CustomUser(AbstractUser):
	email = models.EmailField(
		unique=True,
		blank=True,
	)

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'
		constraints = [
			UniqueConstraint(
				Lower('username'),
				name='unique_username_ci'
			)
		]

class UserProfile(models.Model):
	"""
	Extends the user model with additional fields for the profile.

	- Links to one user (OneToOneField).
	- Stores bio, avatar image, and badge relationships.
	"""
	user = models.OneToOneField(
		to=CustomUser,
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

class UserAppGroup(AuthGroup):
	class Meta:
		proxy = True
		app_label = 'users'
		verbose_name = 'Group'
		verbose_name_plural = 'Groups'