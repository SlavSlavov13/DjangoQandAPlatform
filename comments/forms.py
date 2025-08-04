"""
comments/forms.py

Forms for creating and editing comments.
Each form exposes only the content field for editing via ModelForm.
"""

from django import forms
from .models import Comment

class BaseCommentForm(forms.ModelForm):
	"""
	Abstract form for comment create/edit with content field and media.
	"""
	class Meta:
		model = Comment
		fields = ['content', 'media']

class CommentCreateForm(BaseCommentForm):
	"""
	Form for creating a new comment on a question or answer.
	"""
	pass

class CommentEditForm(BaseCommentForm):
	"""
	Form for editing an existing comment.
	"""
	pass
