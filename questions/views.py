from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
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

class QuestionCreateView(CreateView):
	model = Question
	form_class = QuestionCreateForm
	template_name = "questions/question_form.html"
	success_url = reverse_lazy("questions_list")

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class QuestionUpdateView(UpdateView):
	model = Question
	form_class = QuestionEditForm
	template_name = "questions/question_form.html"
	success_url = reverse_lazy("questions_list")

class QuestionDeleteView(DeleteView):
	model = Question
	template_name = "questions/question_confirm_delete.html"
	success_url = reverse_lazy("questions_list")