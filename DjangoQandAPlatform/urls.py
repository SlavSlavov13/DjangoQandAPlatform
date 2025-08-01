"""
DjangoQandAPlatform/urls.py

Top-level URL routing for the DjangoQandAPlatform project.

- Redirects the root ('') to the main questions list.
- Includes URLs for the API, admin, user auth, answers, questions, comments, and badges apps.
- Serves uploaded media files during development if DEBUG is True.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    # Redirect root to questions list (main page)
    path('', lambda request: redirect('questions-list', permanent=True)),

    # API endpoints (REST)
    path('api/', include('api.urls')),

    # Django admin interface
    path('admin/', admin.site.urls),

    # User authentication and profile
    path('auth/', include('users.urls')),

    # Answers app (CRUD for answers)
    path('answers/', include('answers.urls')),

    # Questions app (CRUD for questions and search/list/detail)
    path('questions/', include('questions.urls')),

    # Comments app (generic comments for questions/answers)
    path('comments/', include('comments.urls')),

    # Badges app (view earned badges and badge catalog)
    path('badges/', include('badges.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
