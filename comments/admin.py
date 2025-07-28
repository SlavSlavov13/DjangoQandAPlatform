# comments/admin.py
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
	list_display = ('author', 'content_object', 'content', 'created_at')
	search_fields = ('author__user__username', 'content')
	list_filter = ('created_at',)
	autocomplete_fields = ('author',)
	readonly_fields = ('content_type', 'object_id', 'content_object', 'author', 'created_at')

	def has_add_permission(self, request, obj=None):
		# Prevent creation of Comment in the admin.
		return False
