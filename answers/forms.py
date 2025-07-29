from django import forms
from .models import Answer

class BaseAnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ['content']

class AnswerCreateForm(BaseAnswerForm):
	...

class AnswerEditForm(BaseAnswerForm):
	...