from django.contrib import admin
from django.utils.html import format_html
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('title', 'author_link', 'created_at', 'updated_at')
	search_fields = ('title', 'body', 'author__user__username')
	list_filter = ('created_at', 'tags')
	autocomplete_fields = ('author', 'tags')
	date_hierarchy = 'created_at'
	readonly_fields = ['author']

	def author_link(self, obj):
		url = f"/admin/users/userprofile/{obj.author.pk}/change/"
		return format_html('<a href="{}">{}</a>', url, obj.author)
	author_link.short_description = 'Author'

	def has_add_permission(self, request, obj=None):
		return False

	# Extensive comment:
	# - format_html safely constructs the link to the UserProfile admin "change" page.
	# - Clicking the author’s name in the admin will open the UserProfile for editing.
	# - The method is included in list_display to replace or supplement the plain author field.
