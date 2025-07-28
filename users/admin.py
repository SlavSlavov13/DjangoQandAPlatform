from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'bio', 'avatar')  # Show these columns in admin list
	search_fields = ('user__username', 'bio')  # Search by username or bio
	list_filter = ('user__is_staff',)  # Filter by staff status if desired
	readonly_fields = ('user',)  # Prevent manual changing of linked User

	def has_add_permission(self, request, obj=None):
		return False


admin.site.unregister(Group)

class NoAddGroupAdmin(GroupAdmin):
	def has_add_permission(self, request):
		return False

	def has_delete_permission(self, request, obj=None):
		return False

	def has_change_permission(self, request, obj=None):
		return False

# Register your custom admin:
admin.site.register(Group, NoAddGroupAdmin)


UserModel = get_user_model()

class CustomUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password')}),
		('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
		('Groups', {'fields': ('groups',)}),
		('Account Deactivation', {'fields': ('is_active',)}),
	)

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		super().save_model(request, obj, form, change)
		groups = form.cleaned_data.get('groups')
		obj.groups.set(groups)  # set expects a list/iterable

admin.site.unregister(UserModel)
admin.site.register(UserModel, CustomUserAdmin)

