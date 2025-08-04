"""
questions/forms.py

Forms for creating and editing Question objects.
Exposes title, tags, and body for both create and edit via BaseQuestionForm.
"""

from django import forms
from .models import Question

class BaseQuestionForm(forms.ModelForm):
	"""Abstract form for create/edit question."""
	class Meta:
		model = Question
		fields = ['title', 'tags', 'body', 'media']

class QuestionCreateForm(BaseQuestionForm):
	"""Form for creating a question."""
	pass

class QuestionEditForm(BaseQuestionForm):
	"""Form for editing a question."""
	pass
