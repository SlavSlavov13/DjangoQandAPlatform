"""
badges/urls.py

Routing for badge detail pages.
"""

from django.urls import path
from badges.views import BadgeDetailsView

urlpatterns = [
	# Route for badge details; expects badge_slug in the URL
	path('<slug:badge_slug>/', BadgeDetailsView.as_view(), name='badge-details'),
]
