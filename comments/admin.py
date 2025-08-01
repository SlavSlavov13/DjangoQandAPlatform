"""
comments/admin.py

Admin configuration for Comment management.
Customizes display, search, and permissions for comment moderation.
"""

from django.contrib import admin
from django.utils.text import Truncator
from django.urls import reverse
from django.utils.html import format_html

from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	"""
	Admin list and form customizations for comments,
	including support for nested comments.
	"""
	list_display = (
		'truncated_content',
		'related_object_link',
		'author_link',
		'created_at',
	)
	search_fields = ('author__username', 'content')
	list_filter = ('created_at', 'content_type')  # Added content_type filter for easier moderation
	autocomplete_fields = ('author',)

	def truncated_content(self, obj):
		return Truncator(obj.content).chars(50)
	truncated_content.short_description = 'Content'

	def author_link(self, obj):
		"""
		Links to the related user profile in admin.
		"""
		url = reverse('admin:auth_user_change', args=[obj.author.pk])
		return format_html('<a href="{}">{}</a>', url, obj.author)
	author_link.short_description = 'Author'

	def related_object_link(self, obj):
		"""
		Displays a clickable link to the related Question, Answer, or Comment in the admin.
		Shows 'Comment (Parent)' when the related object is a comment.
		"""
		if not obj.content_object:
			return '-'
		ct = obj.content_type
		try:
			app_label = ct.app_label
			model = ct.model
			object_id = obj.object_id
			url = reverse(f'admin:{app_label}_{model}_change', args=[object_id])
			if model == 'comment':
				model_name = 'Comment (Parent)'
			else:
				model_name = model.capitalize()
			obj_str = str(obj.content_object)
			return format_html('<a href="{}">{}: {}</a>', url, model_name, obj_str)
		except Exception:
			# Show string representation if reverse fails.
			return str(obj.content_object)
	related_object_link.short_description = 'Related Object'
	related_object_link.admin_order_field = 'content_type'

	def get_readonly_fields(self, request, obj=None):
		# Make important fields read-only for Staff Moderators to prevent edits.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['author', 'created_at', 'related_object_link']
		return []

	def get_exclude(self, request, obj=None):
		# Hide certain fields for Staff Moderators for safety.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['content_type', 'object_id']
		return []

	def has_add_permission(self, request, obj=None):
		# Prevent in-admin creation of comments by Staff Moderators.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True
