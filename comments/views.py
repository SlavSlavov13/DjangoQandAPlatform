"""
comments/views.py

Views for adding, editing, and deleting comments on questions, answers, and comments.
Handles permissions, context logic, and redirections.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView, CreateView, DeleteView

from DjangoQandAPlatform.mixins import UserIsAuthorMixin
from .forms import CommentCreateForm, CommentEditForm
from .models import Comment
from .utils import get_comment_context, get_root_question


class AddCommentView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = CommentCreateForm
	template_name = 'comments/comment_form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_comment_context(self.kwargs))
		return context

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		# Determine content_type and object_id based on URL kwargs
		content_type = None
		object_id = None

		if self.kwargs.get('answer_id'):
			content_type = ContentType.objects.get(app_label='answers', model='answer')
			object_id = self.kwargs['answer_id']

		elif self.kwargs.get('question_id'):
			content_type = ContentType.objects.get(app_label='questions', model='question')
			object_id = self.kwargs['question_id']

		elif self.kwargs.get('comment_id') or self.kwargs.get('parent_comment_id'):
			content_type = ContentType.objects.get(app_label='comments', model='comment')
			object_id = self.kwargs.get('comment_id') or self.kwargs.get('parent_comment_id')

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
		# Redirect to the root question details
		question = get_root_question(form.instance.content_object)
		if question:
			return redirect('question_details', pk=question.pk)
		else:
			return redirect('home')


class EditCommentView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
	model = Comment
	form_class = CommentEditForm
	pk_url_kwarg = 'comment_id'
	template_name = 'comments/comment_form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_comment_context(self.kwargs))
		context['exists'] = True
		return context

	def get_success_url(self):
		comment = self.get_object()
		question = get_root_question(comment.content_object)
		if question:
			return reverse('question_details', kwargs={'pk': question.pk})
		else:
			return reverse('home')


class CommentDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
	model = Comment
	template_name = "comments/comment_confirm_delete.html"
	pk_url_kwarg = 'comment_id'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context.update(get_comment_context(self.kwargs))
		context['exists'] = True
		return context

	def get_success_url(self):
		comment = self.get_object()
		question = get_root_question(comment.content_object)
		if question:
			return reverse('question_details', kwargs={'pk': question.pk})
		else:
			return reverse('home')