from django import forms
from .models import Question

class BaseQuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['title', 'body']

class QuestionCreateForm(BaseQuestionForm):
	...

class QuestionEditForm(BaseQuestionForm):
	...
