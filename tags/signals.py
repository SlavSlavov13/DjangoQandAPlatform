from django.db import transaction
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tag, InitialSetup


@receiver(post_migrate)
def create_default_tags_once(sender, **kwargs):
	with transaction.atomic():
		# Check or create flag row
		flag, created = InitialSetup.objects.get_or_create(pk=1)
		if flag.tags_created:
			return  # Already created tags before: skip

		default_tags = ['Python', 'Django', 'WebDev', 'Database', 'API']
		for name in default_tags:
			Tag.objects.get_or_create(name=name)

		flag.tags_created = True
		flag.save()
