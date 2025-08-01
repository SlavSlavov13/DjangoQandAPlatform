"""
comments/views.py

Views for adding, editing, and deleting comments on questions, answers, and comments.
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
	Create a comment on a question, answer, or another comment.
	The parent object is determined by URL kwargs.
	"""
	model = Comment
	form_class = CommentCreateForm
	template_name = 'comments/comment_form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		# Handle comment id or parent_comment_id from URLs
		comment_id = self.kwargs.get('comment_id') or self.kwargs.get('parent_comment_id')

		context['exists'] = False

		if question_id:
			question = get_object_or_404(Question, pk=question_id)
			context['question_title'] = question.title
			context['question_id'] = question_id
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['question_title'] = answer.question.title
			context['question_id'] = answer.question.pk
		elif comment_id:
			comment = get_object_or_404(Comment, pk=comment_id)
			# Attempt to get the root question for context
			parent_obj = comment.content_object
			root_question = None
			while True:
				if isinstance(parent_obj, Question):
					root_question = parent_obj
					break
				if isinstance(parent_obj, Answer):
					root_question = parent_obj.question
					break
				if isinstance(parent_obj, Comment):
					parent_obj = parent_obj.content_object
				else:
					break
			if root_question:
				context['question_title'] = root_question.title
				context['question_id'] = root_question.pk
			else:
				context['question_title'] = "Nested Comment"
				context['question_id'] = None
			context['parent_comment'] = comment.content_object
		else:
			context['question_title'] = ''
			context['question_id'] = None

		if answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['answer_id'] = answer_id
			context['answer_excerpt'] = answer.content[:120]
		else:
			context['answer_id'] = None
			context['answer_excerpt'] = ''

		return context

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')
		comment_id = self.kwargs.get('comment_id') or self.kwargs.get('parent_comment_id')

		if answer_id:
			content_type = ContentType.objects.get(app_label='answers', model='answer')
			object_id = answer_id
		elif question_id:
			content_type = ContentType.objects.get(app_label='questions', model='question')
			object_id = question_id
		elif comment_id:
			content_type = ContentType.objects.get(app_label='comments', model='comment')
			object_id = comment_id
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
		comment_id = self.kwargs.get('comment_id') or self.kwargs.get('parent_comment_id')

		if question_id:
			redirect_question_id = question_id
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			redirect_question_id = answer.question.pk
		elif comment_id:
			comment = get_object_or_404(Comment, pk=comment_id)
			parent = comment.content_object
			redirect_question_id = None
			while True:
				if isinstance(parent, Question):
					redirect_question_id = parent.pk
					break
				if isinstance(parent, Answer):
					redirect_question_id = parent.question.pk
					break
				if isinstance(parent, Comment):
					parent = parent.content_object
				else:
					break
			if redirect_question_id is None:
				# fallback or error handling
				return redirect('/')
		else:
			return redirect('/')

		return redirect('question_details', pk=redirect_question_id)


class EditCommentView(LoginRequiredMixin, UpdateView):
	"""
	View for editing a comment by its author.
	Handles comments on questions, answers, or other comments.
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
		comment_id = self.kwargs.get('comment_id')

		context['exists'] = True

		if question_id:
			question = get_object_or_404(Question, pk=question_id)
			context['question_title'] = question.title
			context['question_id'] = question_id
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['question_title'] = answer.question.title
			context['question_id'] = answer.question.pk
		elif comment_id:
			comment = get_object_or_404(Comment, pk=comment_id)
			parent_obj = comment.content_object
			root_question = None
			while True:
				if isinstance(parent_obj, Question):
					root_question = parent_obj
					break
				if isinstance(parent_obj, Answer):
					root_question = parent_obj.question
					break
				if isinstance(parent_obj, Comment):
					parent_obj = parent_obj.content_object
				else:
					break
			if root_question:
				context['question_title'] = root_question.title
				context['question_id'] = root_question.pk
			else:
				context['question_title'] = "Nested Comment"
				context['question_id'] = None
			context['parent_comment'] = comment.content_object
		else:
			context['question_title'] = ''
			context['question_id'] = None

		if answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['answer_id'] = answer_id
			context['answer_excerpt'] = answer.content[:120]
		else:
			context['answer_id'] = None
			context['answer_excerpt'] = ''

		return context

	def get_success_url(self):
		comment = self.get_object()
		parent = comment.content_object

		while True:
			if isinstance(parent, Question):
				return reverse('question_details', kwargs={'pk': parent.pk})
			if isinstance(parent, Answer):
				return reverse('question_details', kwargs={'pk': parent.question.pk})
			if isinstance(parent, Comment):
				parent = parent.content_object
			else:
				break
		return reverse('home')  # fallback


class CommentDeleteView(LoginRequiredMixin, DeleteView):
	"""
	Confirmation and logic for deleting a comment by its author.
	Handles comments on questions, answers, or comments.
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
		comment_id = self.kwargs.get('comment_id')

		context['exists'] = True

		if question_id:
			question = get_object_or_404(Question, pk=question_id)
			context['question_title'] = question.title
			context['question_id'] = question_id
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['question_title'] = answer.question.title
			context['question_id'] = answer.question.pk
		elif comment_id:
			comment = get_object_or_404(Comment, pk=comment_id)
			parent_obj = comment.content_object
			root_question = None
			while True:
				if isinstance(parent_obj, Question):
					root_question = parent_obj
					break
				if isinstance(parent_obj, Answer):
					root_question = parent_obj.question
					break
				if isinstance(parent_obj, Comment):
					parent_obj = parent_obj.content_object
				else:
					break
			if root_question:
				context['question_title'] = root_question.title
				context['question_id'] = root_question.pk
			else:
				context['question_title'] = "Nested Comment"
				context['question_id'] = None
			context['parent_comment'] = comment.content_object
		else:
			context['question_title'] = ''
			context['question_id'] = None

		if answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			context['answer_id'] = answer_id
			context['answer_excerpt'] = answer.content[:120]
		else:
			context['answer_id'] = None
			context['answer_excerpt'] = ''

		return context

	def get_success_url(self):
		comment = self.get_object()
		parent = comment.content_object

		while True:
			if isinstance(parent, Question):
				return reverse('question_details', kwargs={'pk': parent.pk})
			if isinstance(parent, Answer):
				return reverse('question_details', kwargs={'pk': parent.question.pk})
			if isinstance(parent, Comment):
				parent = parent.content_object
			else:
				break
		return reverse('home')  # fallback
