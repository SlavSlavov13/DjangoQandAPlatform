"""
badges/apps.py

Django app configuration for the badges app.
"""

from django.apps import AppConfig

class BadgesConfig(AppConfig):
    """
    Config for the badges app (auto field and label).
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'badges'
