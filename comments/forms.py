from django import forms
from .models import Comment
from django.core.exceptions import ValidationError

class BaseCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['content']


class CommentCreateForm(BaseCommentForm):
	...

class CommentEditForm(BaseCommentForm):
	...
