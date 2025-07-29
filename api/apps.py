"""
api/apps.py

Django app configuration for the API app.
"""

from django.apps import AppConfig

class ApiConfig(AppConfig):
    """
    Configuration for the API Django app.
    Sets the app label and auto field type.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
