"""
badges/admin.py

Admin interface configuration for Badge objects.
Provides search, list, and slug prepopulation.
"""

from django.contrib import admin
from django.utils.text import Truncator

from .models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
	"""
	Defines how badges are displayed and managed in the Django admin.
	"""
	list_display = ('name', 'truncated_desc', 'icon')
	search_fields = ('name', 'description')
	prepopulated_fields = {'slug': ('name',)}  # Auto-generate slugs from name.

	def truncated_desc(self, obj):
		return Truncator(obj.description).chars(50)
	truncated_desc.short_description = 'Description'

	# Prepopulated fields prevent manual slug entry errors.
