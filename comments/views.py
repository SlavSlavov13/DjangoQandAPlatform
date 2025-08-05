"""
comments/views.py

Views for adding, editing, and deleting comments on questions, answers, and comments.
Handles permissions, context logic, and redirections.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
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

	def dispatch(self, request, *args, **kwargs):
		"""
		Prevent access to adding comments on disallowed nested comment structures before showing the form,
		specifically disallowing:
		- comments on comments on answers
		- comments on comments on comments on questions (second-level nesting)
		"""
		parent_comment_id = kwargs.get('comment_id') or kwargs.get('parent_comment_id')
		if parent_comment_id:
			try:
				parent_comment = Comment.objects.get(pk=parent_comment_id)
			except Comment.DoesNotExist:
				raise PermissionDenied("Invalid parent comment.")

			parent_ct = parent_comment.content_type
			parent_obj = parent_comment.content_object

			if (
					(parent_ct.app_label == 'answers' and parent_ct.model == 'answer')  # comment on comment on answer
					or (
					parent_ct.app_label == 'comments'
					and getattr(parent_obj, 'content_type', None)
					and parent_obj.content_type.app_label == 'questions'
					and parent_obj.content_type.model == 'question'  # comment on comment on comment on question
			)
			):
				raise PermissionDenied("Nested comments are not allowed.")

		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		self.object = None
		form = self.get_form()

		content_type = None
		object_id = None

		if self.kwargs.get('answer_id'):
			content_type = ContentType.objects.get(app_label='answers', model='answer')
			object_id = self.kwargs['answer_id']

		elif self.kwargs.get('question_id'):
			content_type = ContentType.objects.get(app_label='questions', model='question')
			object_id = self.kwargs['question_id']

		elif self.kwargs.get('comment_id') or self.kwargs.get('parent_comment_id'):
			parent_comment_id = self.kwargs.get('comment_id') or self.kwargs.get('parent_comment_id')
			content_type = ContentType.objects.get(app_label='comments', model='comment')
			object_id = parent_comment_id

			try:
				parent_comment = Comment.objects.get(pk=parent_comment_id)
			except Comment.DoesNotExist:
				return self.handle_no_permission()

			pc_ct = parent_comment.content_type
			pc_obj = parent_comment.content_object

			if (
					(pc_ct.app_label == 'answers' and pc_ct.model == 'answer')
					or (
					pc_ct.app_label == 'comments'
					and pc_obj.content_type.app_label == 'questions'
					and pc_obj.content_type.model == 'question'
			)
			):
				raise PermissionDenied("Nested comments are not allowed.")

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