from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Tag


@receiver(post_migrate)
def create_default_tags_once(sender, **kwargs):
	default_tags = ['Python', 'Django', 'WebDev', 'Database', 'API']
	for name in default_tags:
		Tag.objects.get_or_create(name=name)
