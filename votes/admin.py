# votes/admin.py
from django.contrib import admin
from .models import Vote

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
	list_display = ('user', 'content_object', 'value', 'voted_at')
	list_filter = ('value', 'voted_at')
	search_fields = ('user__user__username',)
	readonly_fields = ('user', 'content_type', 'object_id', 'content_object', 'value', 'voted_at')

	def has_add_permission(self, request, obj=None):
		# Disable the Add button: disallow manual creation
		return False

	def has_change_permission(self, request, obj=None):
		# Optional: Prevent editing existing votes
		return False

	# Extensive comments:
	# - has_add_permission ensures staff cannot fabricate votes.
	# - has_change_permission maintains vote integrity—votes reflect only real user actions.
	# - readonly_fields lock down all data, so no tampering is possible.
