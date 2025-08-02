"""
Signal handlers for the users app.

- Automatically create UserProfile when a user is created.
- Ensure staff group permissions and mutual exclusivity.
- Maintain superuser group membership.
"""
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import transaction
from django.db.models.signals import post_save, post_migrate, m2m_changed
from django.dispatch import receiver
from .models import UserProfile, InitialSetup

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
	"""
	On user creation, create a related UserProfile.
	"""
	if created:
		UserProfile.objects.create(user=instance, bio='')

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
	with transaction.atomic():
		flag, created = InitialSetup.objects.get_or_create(pk=1)
		if flag.groups_created:
			return  # groups already created, skip

		super_admins, _ = Group.objects.get_or_create(name='Super Admins')
		all_permissions = Permission.objects.all()
		super_admins.permissions.set(all_permissions)
		super_admins.save()

		staff_mods_perms_codenames = [
			'view_logentry', 'view_group', 'view_user',
			'change_userprofile', 'view_userprofile',
			'view_question', 'change_question',
			'change_answer', 'view_answer',
			'change_comment', 'view_comment',
			'add_tag', 'change_tag', 'delete_tag', 'view_tag',
			'add_badge', 'change_badge', 'delete_badge', 'view_badge',
		]
		staff_mods, _ = Group.objects.get_or_create(name='Staff Moderators')
		staff_mods_permissions = Permission.objects.filter(codename__in=staff_mods_perms_codenames)
		staff_mods.permissions.set(staff_mods_permissions)
		staff_mods.save()

		# Create a default superuser admin if not exists (optional)
		username = os.environ.get('DEFAULT_ADMIN_USERNAME')
		email = os.environ.get('DEFAULT_ADMIN_EMAIL')
		password = os.environ.get('DEFAULT_ADMIN_PASSWORD')

		if not UserModel.objects.filter(username='admin').exists() and not UserModel.objects.filter(is_superuser=True).exists():
			UserModel.objects.create_superuser(username=username, email=email, password=password)

		flag.groups_created = True
		flag.save()

@receiver(m2m_changed, sender=UserModel.groups.through)
def user_groups_changed(sender, instance, action, **kwargs):
	"""
	Ensure superusers are not also staff moderators, and keep is_staff/is_superuser in sync with groups.

	- If a user is added to both Super Admins and Staff Moderators, remove Staff Moderators.
	- Sets is_superuser and is_staff in line with group membership.
	"""
	if action in ['post_add', 'post_remove', 'post_clear']:
		try:
			super_admins = Group.objects.get(name='Super Admins')
			staff_mods = Group.objects.get(name='Staff Moderators')
		except Group.DoesNotExist:
			return  # Skip update if default groups missing

		user_groups = set(instance.groups.all())
		if super_admins in user_groups and staff_mods in user_groups:
			# Ensure no user is in both at once
			instance.groups.remove(staff_mods)
			user_groups.remove(staff_mods)

		is_superuser = super_admins in user_groups
		is_staff = is_superuser or (staff_mods in user_groups)
		changed = False
		# Defensive: avoid recursion or DB sync issues
		db_user = UserModel.objects.filter(pk=instance.pk).first()
		if db_user:
			if db_user.is_superuser != is_superuser:
				instance.is_superuser = is_superuser
				changed = True
			if db_user.is_staff != is_staff:
				instance.is_staff = is_staff
				changed = True
			if changed:
				instance.save(update_fields=['is_staff', 'is_superuser'])

@receiver(post_save, sender=UserModel)
def assign_superuser_group(sender, instance, created, **kwargs):
	"""
	Ensures all superusers are always in Super Admins group, never Staff Moderators.
	"""
	if instance.is_superuser:
		try:
			super_admin_group = Group.objects.get(name='Super Admins')
			staff_group = Group.objects.get(name='Staff Moderators')
		except Group.DoesNotExist:
			return
		instance.groups.add(super_admin_group)
		if staff_group in instance.groups.all():
			instance.groups.remove(staff_group)

