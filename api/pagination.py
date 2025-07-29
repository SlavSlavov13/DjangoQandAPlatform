"""
api/pagination.py

Custom pagination settings for API responses.
Defines QuestionApiPagination for standard page size and
allows client-specified page size via query parameters.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class QuestionApiPagination(PageNumberPagination):
	"""
	Pagination class for question list endpoints.
	- Default page size: 10
	- Allows client override via ?page_size=
	- Includes page_size in the response for frontend pagination UI
	"""
	page_size = 10
	page_size_query_param = 'page_size'
	max_page_size = 50

	def get_paginated_response(self, data):
		return Response({
			'count': self.page.paginator.count,
			'next': self.get_next_link(),
			'previous': self.get_previous_link(),
			'results': data,
			'page_size': self.get_page_size(self.request),
		})
