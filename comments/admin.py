# comments/admin.py
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'content_object', 'content', 'created_at')
	search_fields = ('author__user__username', 'content')
	list_filter = ('created_at',)
	autocomplete_fields = ('author',)
	readonly_fields = ('content_type', 'object_id', 'content_object', 'author', 'content', 'created_at')

	def has_add_permission(self, request, obj=None):
		# Prevent creation of Comment in the admin.
		return False

	def has_change_permission(self, request, obj=None):
		# Optional: Prevent editing existing Comments in the admin.
		return False

	# Extensive comments:
	# - has_add_permission disables the "Add" button in the admin list and prevents adding.
	# - has_change_permission disables editing; together, these ensure admin is view-only for comments.
	# - readonly_fields make all displayed fields uneditable for extra safety.
