"""
comments/admin.py

Admin configuration for Comment management.
Customizes display, search, and permissions for comment moderation.
"""

from django.contrib import admin
from .models import Comment
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	"""
	Admin list and form customizations for comments.
	"""
	list_display = (
		'content',
		'related_object_link',
		'author_link',
		'created_at',
	)
	search_fields = ('author__username', 'content')
	list_filter = ('created_at',)
	autocomplete_fields = ('author',)

	def author_link(self, obj):
		"""
		Links to the related user profile in admin.
		"""
		url = f"/admin/auth/user/{obj.author.pk}/change/"
		return format_html('<a href="{}">{}</a>', url, obj.author)
	author_link.short_description = 'Author'

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

	def related_object_link(self, obj):
		"""
		Displays a clickable link to the related Question or Answer in the admin.
		"""
		if not obj.content_object:
			return '-'
		ct = obj.content_type
		try:
			app_label = ct.app_label
			model = ct.model
			object_id = obj.object_id
			url = reverse(f'admin:{app_label}_{model}_change', args=[object_id])
			model_name = model.capitalize()
			obj_str = str(obj.content_object)
			return format_html('<a href="{}">{}: {}</a>', url, model_name, obj_str)
		except Exception:
			# Show string representation if reverse fails.
			return str(obj.content_object)
	related_object_link.short_description = 'Related Object'
	related_object_link.admin_order_field = 'content_type'
