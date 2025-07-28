from django.contrib import admin
from django.utils.html import format_html

from .models import Answer

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('question', 'author_link', 'created_at')
	search_fields = ('question__title', 'author__user__username', 'content')
	autocomplete_fields = ('question', 'author')
	raw_id_fields = ('author',)
	readonly_fields = ['author']

	def author_link(self, obj):
		url = f"/admin/users/userprofile/{obj.author.pk}/change/"
		return format_html('<a href="{}">{}</a>', url, obj.author)
	author_link.short_description = 'Author'

	def has_add_permission(self, request, obj=None):
		return False