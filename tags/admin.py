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
	"""
	list_display = ('name',)
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)}

