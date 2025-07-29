"""
Admin configuration for the Tag model.

Provides search, pretty list display, and conditional readonly logic for staff.
"""

from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	"""
	Admin customization for Tag.

	- Shows name in list view.
	- Enables search by name.
	- Auto-populates slug from name during creation.
	- Makes slug readonly for staff moderators but editable for other users.
	"""
	list_display = ('name', )
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)}

	def get_readonly_fields(self, request, obj=None):
		"""
		Makes 'slug' readonly for users in the 'Staff Moderators' group.

		Args:
			request: HttpRequest object.
			obj: Tag instance (or None if adding).

		Returns:
			List of field names to be displayed as readonly.
		"""
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['slug']
		return []
