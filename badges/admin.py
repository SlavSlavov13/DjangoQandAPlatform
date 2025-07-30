"""
badges/admin.py

Admin interface configuration for Badge objects.
Provides search, list, and slug prepopulation.
"""

from django.contrib import admin
from .models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
	"""
	Defines how badges are displayed and managed in the Django admin.
	"""
	list_display = ('name', 'description')
	search_fields = ('name', 'description')
	prepopulated_fields = {'slug': ('name',)}  # Auto-generate slugs from name.

	# Prepopulated fields prevent manual slug entry errors.
