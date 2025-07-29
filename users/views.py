"""
Views for user account lifecycle:
- Registration, profile viewing and editing, login/logout, and AJAX username check.
- Uses CBVs for form-heavy views for clarity and efficiency.
"""

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model, authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.functional import SimpleLazyObject
from django.views import View
from django.views.generic import CreateView, DetailView
from users.forms import UserRegistrationForm, UserEditForm, UserProfileEditForm
from users.models import UserProfile

UserModel = get_user_model()

def unwrap_user(user):
	"""
	Utility to access the real user if passed a Django SimpleLazyObject (occurs in some contexts).
	"""
	if isinstance(user, SimpleLazyObject):
		return user._wrapped
	return user

class UserCreationView(CreateView):
	"""
	Handles user registration with password login.
	Logs the user in after successful registration.
	"""
	model = UserModel
	template_name = 'users/create_user.html'
	form_class = UserRegistrationForm

	def get_success_url(self):
		return reverse('profile-details', args=[self.object.pk])

	def form_valid(self, form):
		response = super().form_valid(form)
		username = form.cleaned_data.get('username')
		raw_password = form.cleaned_data.get('password1')
		user = authenticate(username=username, password=raw_password)
		if user is not None:
			login(self.request, user)
		return response

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('profile-details', request.user.pk)
		return super().dispatch(request, *args, **kwargs)

class EditProfileView(LoginRequiredMixin, View):
	"""
	Allows users to edit their own profile, user info, and change password.
	"""
	template_name = 'users/edit_profile.html'

	def get(self, request):
		user = request.user
		user_profile = UserProfile.objects.get(user=user)
		user_form = UserEditForm(instance=user)
		profile_form = UserProfileEditForm(instance=user_profile)
		password_form = PasswordChangeForm(user=user)
		password_form.fields['old_password'].widget.attrs.pop('autofocus', None)
		return render(request, self.template_name, {
			'user_form': user_form,
			'profile_form': profile_form,
			'password_form': password_form,
		})

	def post(self, request):
		user = request.user
		user_profile = UserProfile.objects.get(user=user)
		if 'update_profile' in request.POST:
			user_form = UserEditForm(request.POST, instance=user)
			profile_form = UserProfileEditForm(request.POST, request.FILES, instance=user_profile)
			password_form = PasswordChangeForm(user=user)
			password_form.fields['old_password'].widget.attrs.pop('autofocus', None)
			if user_form.is_valid() and profile_form.is_valid():
				with transaction.atomic():
					user_form.save()
					profile_form.save()
				return redirect('profile-details', user.id)
		elif 'change_password' in request.POST:
			password_form = PasswordChangeForm(user, request.POST)
			user_form = UserEditForm(instance=user)
			profile_form = UserProfileEditForm(instance=user_profile)
			if password_form.is_valid():
				user = password_form.save()
				return redirect('profile-details', user.id)
		else:
			user_form = UserEditForm(instance=user)
			profile_form = UserProfileEditForm(instance=user_profile)
			password_form = PasswordChangeForm(user=user)

		return render(request, self.template_name, {
			'user_form': user_form,
			'profile_form': profile_form,
			'password_form': password_form,
		})

class ProfileLogoutView(LogoutView):
	"""
	Logs the user out, then redirects to the questions list.
	"""
	template_name = 'users/logout.html'

	def get_success_url(self):
		return reverse_lazy('questions-list')

class ProfileLoginView(LoginView):
	"""
	Logs a user in, and redirects appropriately.
	Prevents re-login for already-logged-in users.
	"""
	template_name = 'users/login.html'

	def get_success_url(self):
		return reverse_lazy('questions-list')

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('profile-details', request.user.pk)
		return super().dispatch(request, *args, **kwargs)

class ProfileDetailView(DetailView):
	"""
	Displays the user's public profile.
	"""
	model = UserModel
	template_name = 'users/user_details.html'
	context_object_name = 'user_obj'

async def check_username(request):
	"""
	AJAX view to check if a username is available.
	Returns JSON.
	"""
	username = request.GET.get('username', '').strip()
	if not username:
		return JsonResponse({'available': False, 'error': 'No username provided.'}, status=400)
	exists = await sync_to_async(UserModel.objects.filter(username=username).exists)()
	return JsonResponse({'available': not exists})
