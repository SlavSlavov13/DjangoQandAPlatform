from django.shortcuts import render
from django.views.generic import DetailView

from badges.models import Badge


# Create your views here.
class BadgeDetailsView(DetailView):
	model = Badge
	template_name = 'badges/badges_details.html'
	slug_url_kwarg = 'badge_slug'