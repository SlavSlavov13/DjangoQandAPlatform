"""
answers/admin.py

Admin configuration for the Answer model including custom display fields and permissions.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Answer

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	"""
	Django admin representation for Answer objects.
	"""
	list_display = ('content', 'question', 'author_link', 'created_at')
	search_fields = ('question__title', 'author__user__username', 'content')
	autocomplete_fields = ('question', 'author')
	raw_id_fields = ('author',)

	def get_readonly_fields(self, request, obj=None):
		# Staff Moderators cannot change author or question.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['author', 'question']
		return []

	def author_link(self, obj):
		# Show an HTML link to the author's profile in Django admin.
		url = f"/admin/users/userprofile/{obj.author.pk}/change/"
		return format_html('{}', url, obj.author)
	author_link.short_description = 'Author'

	def has_add_permission(self, request, obj=None):
		# Staff Moderators cannot add new answers via admin.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True
