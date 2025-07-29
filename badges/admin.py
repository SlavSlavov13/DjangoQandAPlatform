from django.contrib import admin
from .models import Badge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
	list_display = ('name', 'description')
	search_fields = ('name', 'description')

	prepopulated_fields = {'slug': ('name',)}  # Auto-populate slugs from name

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['slug']
		return []
	# Extensive comment: Prepopulated fields prevent manual slug errors.
