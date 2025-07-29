"""
Forms for the users app, covering user registration, editing, and profile changes.

Each form is supplied with a Meta docstring for clarity.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from users.models import UserProfile

UserModel = get_user_model()

class BaseUserForm(forms.ModelForm):
	"""
	Base form for user model, including username, email, and name fields.
	"""
	class Meta:
		model = UserModel
		fields = ['username', 'email', 'first_name', 'last_name']

class UserRegistrationForm(UserCreationForm):
	"""
	Registration form: user creates username, email, password.
	"""
	class Meta:
		model = UserModel
		fields = ['username', 'email', 'password1', 'password2']

class UserEditForm(BaseUserForm):
	"""
	Form for editing basic user details (username/email/names).
	"""
	# Add additional customizations below if needed
	pass

class BaseUserProfileForm(forms.ModelForm):
	"""
	Base form for the user's profile model.
	"""
	class Meta:
		model = UserProfile
		fields = ['bio', 'avatar']

class UserProfileEditForm(BaseUserProfileForm):
	"""
	Form for editing the user's profile (bio/avatar).
	"""
	# Extend or customize as needed
	pass
