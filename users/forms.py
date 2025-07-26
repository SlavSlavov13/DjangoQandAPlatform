# users/forms.py
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import UserProfile

UserModel = get_user_model()


class BaseUserForm(forms.ModelForm):
	class Meta:
		model = UserModel
		fields = ['username', 'email', 'first_name', 'last_name']


class UserRegistrationForm(UserCreationForm):
	class Meta:
		model = UserModel
		fields = ['username', 'email', 'password1', 'password2']


class UserEditForm(BaseUserForm):
	...


class BaseUserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['bio', 'avatar']


class UserProfileEditForm(BaseUserProfileForm):
	...