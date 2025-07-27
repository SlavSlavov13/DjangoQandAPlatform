from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import Answer
from .forms import AnswerCreateForm
from questions.models import Question

class AnswerCreateView(CreateView):
	model = Answer
	form_class = AnswerCreateForm
	template_name = 'answers/add_answer.html'

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
		context['question'] = self.question
		return context
