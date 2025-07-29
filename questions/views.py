from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from answers.models import Answer
from comments.models import Comment
from questions.forms import QuestionCreateForm, QuestionEditForm
from questions.models import Question
from tags.models import Tag


# Create your views here.
class QuestionListView(ListView):
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
	model = Question
	form_class = QuestionCreateForm
	template_name = "questions/question_create_edit.html"
	success_url = reverse_lazy("questions_list")

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
	model = Question
	form_class = QuestionEditForm
	template_name = "questions/question_create_edit.html"

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to edit this question.")
		return obj

	def get_success_url(self):
		return reverse('question_details', args=[self.object.pk])

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
	model = Question
	template_name = "questions/question_confirm_delete.html"
	success_url = reverse_lazy("questions_list")

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to delete this question.")
		return obj

class QuestionDetailView(DetailView):
	model = Question
	template_name = "questions/question_details.html"

	def get_object(self, queryset=None):
		queryset = self.get_queryset().select_related('author')
		return super().get_object(queryset=queryset)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		question = self.object

		# Question-level comments
		comments_on_question = question.comments.select_related('author').order_by('-created_at')

		# Answers with comments prefetched
		answers = Answer.objects.filter(question=question).select_related('author').prefetch_related(
			Prefetch('comments', queryset=Comment.objects.select_related('author').order_by('-created_at'))
		).order_by('-created_at')


		context['comments'] = comments_on_question
		context['answers'] = answers
		return context