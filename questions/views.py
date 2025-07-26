from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from questions.forms import QuestionCreateForm, QuestionEditForm
from questions.models import Question


# Create your views here.
class QuestionListView(ListView):
	model = Question
	template_name = 'questions/questions_list.html'
	context_object_name = 'questions'
	ordering = ['-created_at']
	paginate_by = 10

	def get(self, request, *args, **kwargs):
		page = request.GET.get('page')
		max_page = self.get_paginator(self.get_queryset(), self.paginate_by).num_pages
		try:
			page_num = int(page)
		except (TypeError, ValueError):
			page_num = 1
		if page_num > max_page:
			page_num = max_page

		# redirect or reset request.GET to the capped page_num
		if str(page_num) != page:
			# Redirect to capped page to keep URLs clean
			url = request.path + f'?page={page_num}'
			return redirect(url)

		return super().get(request, *args, **kwargs)


class QuestionCreateView(LoginRequiredMixin, CreateView):
	model = Question
	form_class = QuestionCreateForm
	template_name = "questions/question_form.html"
	success_url = reverse_lazy("questions_list")

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
	model = Question
	form_class = QuestionEditForm
	template_name = "questions/question_form.html"
	success_url = reverse_lazy("questions_list")

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to edit this question.")
		return obj

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
	model = Question
	template_name = "questions/question_confirm_delete.html"
	success_url = reverse_lazy("questions_list")

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to delete this question.")
		return obj