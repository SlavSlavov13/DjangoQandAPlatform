"""
answers/apps.py

Django app configuration for the answers app.
"""
from django.apps import AppConfig

class AnswersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'answers'
