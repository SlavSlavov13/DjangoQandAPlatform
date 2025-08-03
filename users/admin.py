from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group as AuthGroup
from django.urls import reverse
from django.utils.html import format_html_join
from django.utils.text import Truncator

from .models import UserProfile, UserAppGroup


def is_staff_moderator(user):
	"""Check if the user belongs to 'Staff Moderators' group."""
	return user.groups.filter(name='Staff Moderators').exists()

# --- UserProfile admin ---

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
		if is_staff_moderator(request.user):
			return False
		return True

	def get_readonly_fields(self, request, obj=None):
		if is_staff_moderator(request.user):
			return ['user']
		return []

# --- Group admin with restrictions for Staff Moderators ---

# Unregister default Group admin
admin.site.unregister(AuthGroup)

@admin.register(UserAppGroup)
class NoAddGroupAdmin(GroupAdmin):
	"""
	Custom GroupAdmin:
	- Prevents Staff Moderators from adding, deleting, or changing group membership.
	- Other users have normal group permissions.
	"""

	def has_add_permission(self, request, obj=None):
		if is_staff_moderator(request.user):
			return False
		return True

	def has_delete_permission(self, request, obj=None):
		if is_staff_moderator(request.user):
			return False
		return True

	def has_change_permission(self, request, obj=None):
		if is_staff_moderator(request.user):
			return False
		return True

# --- Custom User admin ---

UserModel = get_user_model()

class CustomUserAdmin(UserAdmin):
	"""
	Custom User admin with group link display and per-group restrictions:
	- Shows user groups as links in the admin detail for Staff Moderators
	- Restricts Staff Moderators from deleting users
	"""
	def group_links(self, obj):
		if not obj.pk:
			return "-"
		return format_html_join(
			', ',
			'{}',
			(
				(f'<a href="{reverse("admin:users_userappgroup_change", args=(group.pk,))}">{group.name}</a>',)
				for group in obj.groups.all()
			)
		) or "-"
	group_links.short_description = "Groups"

	def get_fieldsets(self, request, obj=None):
		if is_staff_moderator(request.user):
			fieldsets = super().get_fieldsets(request, obj)
			new_fieldsets = []
			for name, opts in fieldsets:
				fields = list(opts.get('fields', ()))
				if 'groups' in fields and 'group_links' not in fields:
					idx = fields.index('groups')
					fields.insert(idx, 'group_links')
					fields.remove('groups')
				new_opts = {**opts, 'fields': tuple(fields)}
				new_fieldsets.append((name, new_opts))
			return new_fieldsets
		return super().get_fieldsets(request, obj)

	def has_delete_permission(self, request, obj=None):
		if is_staff_moderator(request.user):
			return False
		return True

admin.site.register(UserModel, CustomUserAdmin)
