"""
comments/views.py

Views for adding, editing, and deleting comments on questions and answers.
Handles permissions, context logic, and redirections.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DeleteView
from .forms import CommentCreateForm, CommentEditForm
from questions.models import Question
from answers.models import Answer
from .models import Comment

class AddCommentView(LoginRequiredMixin, CreateView):
	"""
	Create a comment on either a question or an answer.
	The parent object is determined by URL kwargs.
	"""
	model = Comment
	form_class = CommentCreateForm
	template_name = 'comments/comment_form.html'

	def get_context_data(self, **kwargs):
		# Populates template context with question/answer for display.
		context = super().get_context_data(**kwargs)
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		context['exists'] = False
		if question_id:
			question = get_object_or_404(Question, pk=question_id)
			context['question_title'] = question.title
			context['question_id'] = question_id
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['question_title'] = answer.question.title
			context['question_id'] = answer.question.pk
		else:
			context['question_title'] = ''
			context['question_id'] = None

		if answer_id:
			context['answer_id'] = answer_id
			context['answer_excerpt'] = answer.content[:120]
		else:
			context['answer_id'] = None
			context['answer_excerpt'] = ''
		return context

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		answer_id = self.kwargs.get('answer_id')
		question_id = self.kwargs.get('question_id')
		if answer_id:
			content_type = ContentType.objects.get(app_label='answers', model='answer')
			object_id = answer_id
		elif question_id:
			content_type = ContentType.objects.get(app_label='questions', model='question')
			object_id = question_id
		else:
			return self.handle_no_permission()
		form.instance.content_type = content_type
		form.instance.object_id = object_id
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.save()
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		if question_id:
			return redirect('question_details', pk=question_id)
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			return redirect('question_details', pk=answer.question.pk)
		return redirect('questions-list')

class EditCommentView(LoginRequiredMixin, UpdateView):
	"""
	View for editing a comment by its author.
	The comment is found via question or answer context for redirection.
	"""
	model = Comment
	form_class = CommentEditForm
	pk_url_kwarg = 'comment_id'

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to edit this comment.")
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		context['exists'] = True
		if question_id:
			question = get_object_or_404(Question, pk=question_id)
			context['question_title'] = question.title
			context['question_id'] = question_id
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['question_title'] = answer.question.title
			context['question_id'] = answer.question.pk
		else:
			context['question_title'] = ''
			context['question_id'] = None

		if answer_id:
			context['answer_id'] = answer_id
			context['answer_excerpt'] = answer.content[:120]
		else:
			context['answer_id'] = None
			context['answer_excerpt'] = ''
		return context

	def get_success_url(self):
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		if not question_id:
			question_id = get_object_or_404(Answer, pk=answer_id).question.pk
		return reverse('question_details', kwargs={'pk': question_id})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
	"""
	Confirmation and logic for deleting a comment by its author.
	Redirects to question details after successful deletion.
	"""
	model = Comment
	template_name = "comments/comment_confirm_delete.html"
	pk_url_kwarg = 'comment_id'

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to delete this comment.")
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		context['exists'] = True
		if question_id:
			question = get_object_or_404(Question, pk=question_id)
			context['question_title'] = question.title
			context['question_id'] = question_id
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['question_title'] = answer.question.title
			context['question_id'] = answer.question.pk
		else:
			context['question_title'] = ''
			context['question_id'] = None
		if answer_id:
			context['answer_id'] = answer_id
			context['answer_excerpt'] = answer.content[:120]
		else:
			context['answer_id'] = None
			context['answer_excerpt'] = ''
		return context

	def get_success_url(self):
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		if not question_id:
			question_id = get_object_or_404(Answer, pk=answer_id).question.pk
		return reverse('question_details', kwargs={'pk': question_id})
