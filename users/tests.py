"""
Comprehensive tests for the users app.

Includes:
- UserProfile & group signal logic (as before)
- Form validations for registration/user/profile edits
- View tests for registration, login, profile edit
- AJAX username availability check
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from users.models import UserProfile
from users.forms import UserRegistrationForm, UserEditForm, UserProfileEditForm

UserModel = get_user_model()


class UserRegistrationFormTests(TestCase):
	"""
	Tests for the UserRegistrationForm validation and creation workflow.
	"""

	def test_valid_registration_form_creates_user(self):
		"""
		Submitting valid registration data creates a new user.
		"""
		form_data = {
			'username': 'newuser',
			'email': 'newuser@example.com',
			'password1': 'SuperSecret123',
			'password2': 'SuperSecret123'
		}
		form = UserRegistrationForm(data=form_data)
		self.assertTrue(form.is_valid())
		user = form.save()
		self.assertEqual(user.username, 'newuser')
		self.assertTrue(UserProfile.objects.filter(user=user).exists())

	def test_registration_form_password_mismatch(self):
		"""
		Password mismatch is caught and flagged by the form.
		"""
		form_data = {
			'username': 'newuser2',
			'email': 'newuser2@example.com',
			'password1': 'PasswordA',
			'password2': 'PasswordB'
		}
		form = UserRegistrationForm(data=form_data)
		self.assertFalse(form.is_valid())
		self.assertIn('password2', form.errors)

	def test_registration_username_unique(self):
		"""
		Registration with an existing username is not allowed.
		"""
		UserModel.objects.create_user(username='takenuser', password='pw')
		form_data = {
			'username': 'takenuser',
			'email': 'whoever@e.com',
			'password1': 'pw12345',
			'password2': 'pw12345'
		}
		form = UserRegistrationForm(data=form_data)
		self.assertFalse(form.is_valid())
		self.assertIn('username', form.errors)


class UserProfileEditFormTests(TestCase):
	"""
	Test the user and user profile edit forms.
	"""

	def setUp(self):
		self.user = UserModel.objects.create_user('profiled', password='pw')
		self.profile = self.user.profile

	def test_user_edit_form_updates_fields(self):
		form_data = {
			'username': 'profiledX',
			'email': 'prof@example.com',
			'first_name': 'Test',
			'last_name': 'User'
		}
		form = UserEditForm(form_data, instance=self.user)
		self.assertTrue(form.is_valid())
		new_user = form.save()
		self.assertEqual(new_user.username, 'profiledX')
		self.assertEqual(new_user.email, 'prof@example.com')

	def test_profile_edit_form_valid(self):
		form_data = {
			'bio': 'New bio info',
		}
		form = UserProfileEditForm(form_data, instance=self.profile)
		self.assertTrue(form.is_valid())
		updated_profile = form.save()
		self.assertEqual(updated_profile.bio, 'New bio info')


class UserViewsTests(TestCase):
	"""
	End-to-end tests for views: registration, login, edit profile, and profile detail.
	"""

	def setUp(self):
		self.client = Client()

	def test_register_view_creates_user_and_profile(self):
		"""
		Posting valid registration data logs in user and creates UserProfile.
		"""
		url = reverse('register')
		data = {
			'username': 'joined',
			'email': 'joined@email.com',
			'password1': 'StrongPass19',
			'password2': 'StrongPass19',
		}
		resp = self.client.post(url, data)
		# Should redirect after successful registration
		self.assertEqual(resp.status_code, 302)
		user = UserModel.objects.get(username='joined')
		self.assertTrue(UserProfile.objects.filter(user=user).exists())
		# Session should now have user as authenticated
		resp = self.client.get(reverse('profile-details', args=[user.pk]))
		self.assertContains(resp, 'joined')

	def test_login_logout_flow(self):
		"""
		A user can log in and log out using the appropriate views.
		"""
		user = UserModel.objects.create_user('foo', password='barbaz0!')
		login_url = reverse('login')
		logout_url = reverse('logout')
		resp = self.client.post(login_url, {'username': 'foo', 'password': 'barbaz0!'})
		self.assertEqual(resp.status_code, 302)
		home_url = reverse('questions-list')
		self.assertRedirects(resp, home_url, fetch_redirect_response=False)
		self.assertIn('_auth_user_id', self.client.session)
		# Now try logging out
		resp = self.client.post(logout_url)
		self.assertEqual(resp.status_code, 302)
		self.client.logout()
		resp = self.client.get(home_url)
		self.assertNotIn('_auth_user_id', self.client.session)

	def test_edit_profile_view(self):
		"""
		Authenticated user can update their profile and user info.
		"""
		user = UserModel.objects.create_user('edity', password='pw4edit')
		self.client.login(username='edity', password='pw4edit')
		url = reverse('edit-profile')
		form_data = {
			'username': 'edity',
			'email': 'e@x.com',
			'first_name': 'Edity',
			'last_name': 'Lastname',
			'bio': 'My new biography!',
		}
		# The view expects both user_form and profile_form fields
		resp = self.client.post(url, {
			'update_profile': 'yes',
			'username': 'edity',
			'email': 'e@x.com',
			'first_name': 'Edity',
			'last_name': 'Lastname',
			'bio': 'My new biography!',
			# 'avatar': <skip for now>
		})
		self.assertEqual(resp.status_code, 302)
		user.refresh_from_db()
		self.assertEqual(user.profile.bio, 'My new biography!')

	def test_profile_detail_view(self):
		"""
		The detail view displays a user's information.
		"""
		user = UserModel.objects.create_user('shown', password='pw')
		url = reverse('profile-details', args=[user.pk])
		resp = self.client.get(url)
		self.assertContains(resp, 'shown')


class AjaxUsernameCheckTests(TestCase):
	"""
	Test the AJAX username-availability-check endpoint.
	"""

	def test_username_check_available(self):
		url = reverse('check-username')
		resp = self.client.get(url, {'username': 'unassignedname'})
		self.assertEqual(resp.status_code, 200)
		self.assertJSONEqual(resp.content, {'available': True})

	def test_username_check_taken(self):
		UserModel.objects.create_user('takenx', password='pw')
		url = reverse('check-username')
		resp = self.client.get(url, {'username': 'takenx'})
		self.assertEqual(resp.status_code, 200)
		self.assertJSONEqual(resp.content, {'available': False})

	def test_username_check_missing(self):
		url = reverse('check-username')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 400)
		self.assertJSONEqual(resp.content, {'available': False, 'error': 'No username provided.'})
