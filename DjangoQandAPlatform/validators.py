from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class SizeValidator:
	def __init__(self, max_mb=10):
		self.max_size = max_mb * 1024 * 1024  # Convert MB to bytes

	def __call__(self, file):
		if file.size > self.max_size:
			raise ValidationError(f"Maximum file size is {self.max_size // (1024*1024)}MB")

	def __eq__(self, other):
		return isinstance(other, SizeValidator) and self.max_size == other.max_size
