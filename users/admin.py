from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.html import format_html_join

from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'bio', 'avatar')  # Show these columns in admin list
	search_fields = ('user__username', 'bio')  # Search by username or bio
	list_filter = ('user__is_staff',)  # Filter by staff status if desired

	def has_add_permission(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['user',]
		return []


admin.site.unregister(Group)

class NoAddGroupAdmin(GroupAdmin):
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

# Register your custom admin:
admin.site.register(Group, NoAddGroupAdmin)


UserModel = get_user_model()

class CustomUserAdmin(UserAdmin):
	def group_links(self, obj):
		if not obj.pk:
			return "-"
		return format_html_join(
			', ',
			'<a href="{}">{}</a>',
			(
				(
					reverse('admin:auth_group_change', args=(group.pk,)),
					group.name
				)
				for group in obj.groups.all()
			)
		) or "-"
	group_links.short_description = "Groups"
	group_links.allow_tags = True

	def get_fieldsets(self, request, obj=None):
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
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

admin.site.unregister(UserModel)
admin.site.register(UserModel, CustomUserAdmin)


