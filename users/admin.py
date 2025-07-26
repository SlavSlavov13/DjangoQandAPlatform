from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'bio', 'avatar')  # Show these columns in admin list
	search_fields = ('user__username', 'bio')  # Search by username or bio
	list_filter = ('user__is_staff',)  # Filter by staff status if desired
	readonly_fields = ('user',)  # Prevent manual changing of linked User

	# Extensive comment:
	# - readonly_fields locks user relation (prevent data integrity issues).
	# - list_display and search_fields greatly improve findability in the admin.
