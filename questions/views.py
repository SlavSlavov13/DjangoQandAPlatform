"""
questions/views.py

Views for queston listing, creation, update, delete, and detail display.
Handles permission checks, context enrichment, and related fetching.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from DjangoQandAPlatform.mixins import UserIsAuthorMixin
from answers.models import Answer
from comments.models import Comment
from questions.forms import QuestionCreateForm, QuestionEditForm
from questions.models import Question
from tags.models import Tag

class QuestionListView(ListView):
	"""
	List all questions (paginated), with tags in the context for filtering.
	"""
	model = Question
	template_name = 'questions/questions_list.html'
	context_object_name = 'questions'
	ordering = ['-created_at']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['has_questions'] = Question.objects.exists()
		context['tags'] = Tag.objects.all()
		return context

class QuestionCreateView(LoginRequiredMixin, CreateView):
	"""
	Form and submission for new questions. Requires user authentication.
	"""
	model = Question
	form_class = QuestionCreateForm
	template_name = "questions/question_create_edit.html"

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('question_details', args=[self.object.pk])

class QuestionUpdateView(LoginRequiredMixin, UserIsAuthorMixin, UpdateView):
	"""
	Edit an existing question (owner only).
	"""
	model = Question
	form_class = QuestionEditForm
	template_name = "questions/question_create_edit.html"

	def get_success_url(self):
		return reverse('question_details', args=[self.object.pk])

class QuestionDeleteView(LoginRequiredMixin, UserIsAuthorMixin, DeleteView):
	"""
	Delete a user's own question.
	"""
	model = Question
	template_name = "questions/question_confirm_delete.html"
	success_url = reverse_lazy("questions-list")

class QuestionDetailView(DetailView):
	model = Question
	template_name = "questions/question_details.html"

	def get_object(self, queryset=None):
		queryset = self.get_queryset().select_related('author')
		return super().get_object(queryset=queryset)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		question = self.object

		# Prefetch nested comments on each top-level comment for question
		child_comments_prefetch = Prefetch(
			'comments',  # generic relation on Comment (i.e., child comments)
			queryset=Comment.objects.select_related('author').order_by('-created_at'),
			to_attr='fetched_child_comments'
		)

		# Prefetch top-level comments on question + their child comments
		comments_on_question = question.comments.select_related('author').prefetch_related(child_comments_prefetch).order_by('-created_at')

		# Prefetch answers, their authors, their comments, and those comments' child comments
		answers = (
			Answer.objects
			.filter(question=question)
			.select_related('author')
			.prefetch_related(
				Prefetch(
					'comments',
					queryset=Comment.objects.select_related('author').prefetch_related(child_comments_prefetch).order_by('-created_at'),
					to_attr='fetched_comments'
				)
			)
			.order_by('-created_at')
		)

		context['comments'] = comments_on_question  # now each comment has .fetched_child_comments
		context['answers'] = answers  # and each answer has .fetched_comments, each with .fetched_child_comments
		return context