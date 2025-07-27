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


# Create your views here.
class QuestionListView(ListView):
	model = Question
	template_name = 'questions/questions_list.html'
	context_object_name = 'questions'
	ordering = ['-created_at']
	paginate_by = 10

	def get_queryset(self):
		queryset = super().get_queryset()
		q = self.request.GET.get('search')
		if q:
			queryset = queryset.filter(
				Q(title__icontains=q) | Q(body__icontains=q)
			).distinct()
		return queryset

	def get(self, request, *args, **kwargs):
		page = request.GET.get('page')
		max_page = self.get_paginator(self.get_queryset(), self.paginate_by).num_pages
		try:
			page_num = int(page)
		except (TypeError, ValueError):
			page_num = 1
		if page_num > max_page:
			page_num = max_page

		if str(page_num) != page:
			url = request.path + f'?page={page_num}'
			return redirect(url)

		return super().get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['has_questions'] = Question.objects.exists()
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