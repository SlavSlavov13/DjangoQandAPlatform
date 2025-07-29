"""
answers/forms.py

Forms for creating and editing Answer objects.
"""

from django import forms
from .models import Answer

class BaseAnswerForm(forms.ModelForm):
	"""
	Abstract base form for answer create/edit. Only exposes 'content' field.
	"""
	class Meta:
		model = Answer
		fields = ['content']

class AnswerCreateForm(BaseAnswerForm):
	"""Form for creating an answer."""
	pass

class AnswerEditForm(BaseAnswerForm):
	"""Form for editing an answer."""
	pass
