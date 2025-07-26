from django.contrib import admin
from django.utils.html import format_html

from .models import Answer

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
	list_display = ('question', 'author_link', 'is_accepted', 'created_at')
	list_filter = ('is_accepted',)
	search_fields = ('question__title', 'author__user__username', 'content')
	autocomplete_fields = ('question', 'author')
	raw_id_fields = ('author',)

	def author_link(self, obj):
		"""
		Returns an HTML link to the author’s UserProfile in the admin.
		"""
		# obj.author.pk is the UserProfile's primary key
		# 'users_userprofile' = '<app_label>_<modelname>' (all lowercase)
		url = f"/admin/users/userprofile/{obj.author.pk}/change/"
		# Display the username as the clickable text
		return format_html('<a href="{}">{}</a>', url, obj.author)
	author_link.short_description = 'Author'  # Sets the admin column header

	# Extensive comment: Use autocomplete and raw_id for high-volume relations.
