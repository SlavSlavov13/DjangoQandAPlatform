from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Answer
from .forms import AnswerCreateForm, AnswerEditForm
from questions.models import Question

class AnswerCreateView(LoginRequiredMixin, CreateView):
	model = Answer
	form_class = AnswerCreateForm
	template_name = 'answers/answer.html'

	def dispatch(self, request, *args, **kwargs):
		self.question = get_object_or_404(Question, id=kwargs['question_id'])
		return super().dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		answer = form.save(commit=False)
		answer.author = self.request.user
		answer.question = self.question
		answer.save()
		return super().form_valid(form)

	def get_success_url(self):
		return reverse('question_details', kwargs={'pk': self.question.id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['exists'] = False
		context['question'] = self.question
		return context

class AnswerEditView(LoginRequiredMixin, UpdateView):
	model = Answer
	form_class = AnswerEditForm
	template_name = 'answers/answer.html'
	pk_url_kwarg = 'answer_id'

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to edit this answer.")
		return obj

	def dispatch(self, request, *args, **kwargs):
		question_id = Answer.objects.get(id=kwargs['answer_id']).question.id
		self.question = get_object_or_404(Question, id=question_id)
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		return reverse('question_details', kwargs={'pk': self.question.id})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['exists'] = True
		context['question'] = self.question
		return context

class AnswerDeleteView(LoginRequiredMixin, DeleteView):
	model = Answer
	template_name = "answers/answers_confirm_delete.html"
	pk_url_kwarg = 'answer_id'

	def get_object(self, queryset=None):
		obj = super().get_object(queryset)
		if obj.author != self.request.user:
			raise PermissionDenied("You do not have permission to delete this answer.")
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		answer = self.object
		question_id = answer.question.id
		question = get_object_or_404(Question, id=question_id)
		context['question_title'] = question.title
		context['question_id'] = question_id
		context['answer_excerpt'] = answer.content[:120]

		return context

	def get_success_url(self):
		question_id = self.object.question.id

		return reverse('question_details', kwargs={'pk': question_id})
