from django.core.exceptions import PermissionDenied


class UserIsAuthorMixin:
	"""
	Mixin to verify that the requesting user is the author of the object.
	"""

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to modify this object.")
		return obj