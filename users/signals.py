from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save, post_migrate, m2m_changed
from django.dispatch import receiver
from .models import UserProfile


UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance, bio='')

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
	super_admins, created = Group.objects.get_or_create(name='Super Admins')
	all_permissions = Permission.objects.all()
	super_admins.permissions.set(all_permissions)
	super_admins.save()

	staff_mods, created = Group.objects.get_or_create(name='Staff Moderators')


@receiver(m2m_changed, sender=UserModel.groups.through)
def user_groups_changed(sender, instance, action, **kwargs):
	if action in ['post_add', 'post_remove', 'post_clear']:
		try:
			super_admins = Group.objects.get(name='Super Admins')
			staff_mods = Group.objects.get(name='Staff Moderators')
		except Group.DoesNotExist:
			return

		user_groups = set(instance.groups.all())

		if super_admins in user_groups and staff_mods in user_groups:
			# User is in both groups - remove staff_mods group
			instance.groups.remove(staff_mods)
			user_groups.remove(staff_mods)

		is_superuser = super_admins in user_groups
		is_staff = is_superuser or (staff_mods in user_groups)

		changed = False
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
	if instance.is_superuser:
		group = Group.objects.get(name='Super Admins')
		staff_group = Group.objects.get(name='Staff Moderators')
		instance.groups.add(group)
		if staff_group in instance.groups.all():
			instance.groups.remove(staff_group)
