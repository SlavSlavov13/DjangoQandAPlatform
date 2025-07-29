"""
App configuration for the users Django app.
Automatically connects signal handlers.
"""

from django.apps import AppConfig

class UsersConfig(AppConfig):
    """
    Django AppConfig for users app.

    - Imports signals when app is ready to ensure user/profile syncing.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        """
        Imports users.signals to connect signal handlers.
        """
        import users.signals  # noqa: F401
