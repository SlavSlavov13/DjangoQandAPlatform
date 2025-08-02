"""
App configuration for the tags application.
"""

from django.apps import AppConfig

class TagsConfig(AppConfig):
    """
    AppConfig for tags app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tags'

    def ready(self):
        import tags.signals
