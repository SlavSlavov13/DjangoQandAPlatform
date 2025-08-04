"""
answers/admin.py

Admin configuration for the Answer model including custom display fields and permissions.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import Truncator

from .models import Answer

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	"""
	Django admin representation for Answer objects.
	"""
	list_display = ('truncated_content', 'question_link', 'author_link', 'created_at')
	search_fields = ('question__title', 'author__user__username', 'content')
	autocomplete_fields = ('question', 'author')
	raw_id_fields = ('author',)

	def truncated_content(self, obj):
		return Truncator(obj.content).chars(50)
	truncated_content.short_description = 'Content'

	def get_readonly_fields(self, request, obj=None):
		# Staff Moderators cannot change author or question.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['author', 'question']
		return []

	def author_link(self, obj):
		"""
		Links to the related user profile in admin.
		"""
		url = f"/admin/users/customuser/{obj.author.pk}/change/"
		return format_html('<a href="{}">{}</a>', url, obj.author)
	author_link.short_description = 'Author'

	def question_link(self, obj):
		"""
		Links to the related question in admin.
		"""
		url = f"/admin/questions/question/{obj.question.pk}/change/"
		return format_html('<a href="{}">{}</a>', url, Truncator(obj.question).chars(50))
	question_link.short_description = 'Question'

	def has_add_permission(self, request, obj=None):
		# Staff Moderators cannot add new answers via admin.
		if request.user.groups.filter(name='Staff Moderators').exists():
			return False
		return True
