"""
badges/views.py

Badge detail view for showing badge information to users.
"""

from django.views.generic import DetailView
from badges.models import Badge

class BadgeDetailsView(DetailView):
	"""
	Displays detailed information about a single badge.
	Badge is looked up by slug in the URL.
	"""
	model = Badge
	template_name = 'badges/badges_details.html'
	slug_url_kwarg = 'badge_slug'
