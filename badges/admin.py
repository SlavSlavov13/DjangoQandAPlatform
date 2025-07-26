from django.contrib import admin
from .models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'icon')
	search_fields = ('name', 'description')

	# Extensive comment: Keep list_display and search_fields focused for admin clarity.
