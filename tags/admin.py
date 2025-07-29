from django.contrib import admin
from .models import Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name', )
	search_fields = ('name',)
	prepopulated_fields = {'slug': ('name',)}

	def get_readonly_fields(self, request, obj=None):
		if request.user.groups.filter(name='Staff Moderators').exists():
			return ['slug']
		return []
