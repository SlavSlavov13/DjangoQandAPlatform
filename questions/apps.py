"""
questions/apps.py

AppConfig for the questions app.
"""

from django.apps import AppConfig

class QuestionsConfig(AppConfig):
    """App configuration for questions."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'questions'
