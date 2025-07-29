# comments/admin.py
from django.contrib import admin
from .models import Comment
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = (
		'content',
		'related_object_link',
		'author',
		'created_at',
	)
	search_fields = ('author__username', 'content')
	list_filter = ('created_at',)
	autocomplete_fields = ('author',)

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['author', 'created_at', 'related_object_link']
		return []

	def get_exclude(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['content_type', 'object_id']
		return []


	def has_add_permission(self, request, obj=None):
		# Prevent creation of Comment in the admin.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

	def related_object_link(self, obj):
		"""Shows a clickable link to the related Question or Answer in the admin."""
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
			# If reverse fails, just show the string representation
			return str(obj.content_object)

	related_object_link.short_description = 'Related Object'
	related_object_link.admin_order_field = 'content_type'