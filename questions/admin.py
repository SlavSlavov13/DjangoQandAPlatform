"""
questions/admin.py

Admin configuration for managing Question objects.
Defines list, filter, and search behaviors for Django admin.
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import Truncator

from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	"""
	Custom admin for Question: adds clickable author link, disables add for staff moderators.
	"""
	list_display = ['truncated_title', 'author_link', 'created_at']
	search_fields = ('title', 'body', 'author__user__username')
	list_filter = ('created_at', 'tags')
	autocomplete_fields = ('author', 'tags')
	date_hierarchy = 'created_at'

	def truncated_title(self, obj):
		return Truncator(obj.title).chars(50)
	truncated_title.short_description = 'Title'

	def author_link(self, obj):
		"""
		Links to the related user profile in admin.
		"""
		url = f"/admin/users/customuser/{obj.author.pk}/change/"
		return format_html('<a href="{}">{}</a>', url, obj.author)
	author_link.short_description = 'Author'

	def has_add_permission(self, request, obj=None):
		"""
		Disables add for Staff Moderators group.
		"""
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True

	def get_readonly_fields(self, request, obj=None):
		"""
		Makes author field read-only for Staff Moderators.
		"""
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['author']
		return []
