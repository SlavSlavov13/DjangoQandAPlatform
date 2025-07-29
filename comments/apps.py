"""
comments/apps.py

App configuration for the comments app.
"""

from django.apps import AppConfig

class CommentsConfig(AppConfig):
    """
    Configuration for the comments application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comments'
