"""
Admin configuration for the users app.

- Customizes admin for UserProfile and Group (with permission logic for 'Staff Moderators').
- Customizes admin for the User model, including group display and per-group restrictions.

How 'Staff Moderators' restrictions work is explained in each class/method.
"""

from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.text import Truncator

from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	"""
	Admin for user profiles, with search and display customizations.

	- Prevents Staff Moderators from adding profiles.
	- Makes primary user field read-only for Staff Moderators.
	"""
	list_display = ('user', 'truncated_bio', 'avatar')
	search_fields = ('user__username', 'bio')
	list_filter = ('user__is_staff',)

	def truncated_bio(self, obj):
		return Truncator(obj.bio).chars(50)
	truncated_bio.short_description = 'Bio'

	def has_add_permission(self, request, obj=None):
		"""
		Prevents Staff Moderators from adding user profiles.
		"""
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

	def get_readonly_fields(self, request, obj=None):
		"""
		Makes user field read-only for Staff Moderators.
		"""
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['user']
		return []

# --- Group Admin Restriction for Staff Moderators ---

admin.site.unregister(Group)

class NoAddGroupAdmin(GroupAdmin):
	"""
	Custom GroupAdmin:
	- Prevents Staff Moderators from adding, deleting, or changing group membership.
	- Other users have normal group permissions.
	"""

	def has_add_permission(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

	def has_delete_permission(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

	def has_change_permission(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

admin.site.register(Group, NoAddGroupAdmin)

# -- User admin modifications --

UserModel = get_user_model()

class CustomUserAdmin(UserAdmin):
	"""
	Custom User admin with group link display and per-group restrictions:

	- Shows user groups as links in the admin detail for Staff Moderators
	- Restricts Staff Moderators from deleting users
	"""
	def group_links(self, obj):
		"""
		Returns HTML with clickable group names for each group the user belongs to.
		(For display in admin.)
		"""
		if not obj.pk:
			return "-"
		# Groups as links to their admin change pages
		return format_html_join(
			', ',
			'{}',
			(
				(f'<a href="{reverse("admin:auth_group_change", args=(group.pk,))}">{group.name}</a>',)
				for group in obj.groups.all()
			)
		) or "-"
	group_links.short_description = "Groups"
	group_links.allow_tags = True

	def get_fieldsets(self, request, obj=None):
		"""
		For Staff Moderators, replaces group selection with just a group display.
		"""
		if request.user.groups.filter(name='Staff Moderators').exists():
			fieldsets = super().get_fieldsets(request, obj)
			new_fieldsets = []
			for name, opts in fieldsets:
				fields = list(opts['fields']) if 'fields' in opts else []
				if 'groups' in fields and 'group_links' not in fields:
					idx = fields.index('groups')
					fields.insert(idx, 'group_links')
					fields.remove('groups')
				opts = {**opts, 'fields': tuple(fields)}
				new_fieldsets.append((name, opts))
			return new_fieldsets
		return super().get_fieldsets(request, obj)

	def has_delete_permission(self, request, obj=None):
		"""
		Staff Moderators cannot delete users.
		"""
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

admin.site.unregister(UserModel)
admin.site.register(UserModel, CustomUserAdmin)
