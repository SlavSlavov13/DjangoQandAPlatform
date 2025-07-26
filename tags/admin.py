from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)}  # Auto-populate slugs from name

	# Extensive comment: Prepopulated fields prevent manual slug errors.
