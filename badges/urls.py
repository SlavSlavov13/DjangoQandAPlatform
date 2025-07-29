from django.urls import path

from badges.views import BadgeDetailsView

urlpatterns = [
	path('<slug:badge_slug>/', BadgeDetailsView.as_view(), name='badge-details')
]