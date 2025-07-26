# notifications/admin.py
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = ('user', 'message', 'created_at', 'read', 'url')
	list_filter = ('read', 'created_at')
	search_fields = ('user__user__username', 'message')
	readonly_fields = ('user', 'message', 'created_at', 'read', 'url')

	def has_add_permission(self, request, obj=None):
		# Disables the Add button in admin
		return False

	def has_change_permission(self, request, obj=None):
		# Optional: Prevent editing existing notifications for integrity
		return False

	# Extensive comments:
	# - has_add_permission prevents accidental or manual notification creation.
	# - has_change_permission ensures notifications reflect true platform state and history.
	# - readonly_fields lock down critical data for audit and trust.
