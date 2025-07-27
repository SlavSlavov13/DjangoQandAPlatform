from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import FormView
from .forms import CommentCreateForm
from questions.models import Question
from answers.models import Answer


class AddCommentView(LoginRequiredMixin, FormView):
	form_class = CommentCreateForm
	template_name = 'comments/comment_form.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')

		if question_id:
			from questions.models import Question
			question = Question.objects.get(pk=question_id)
			context['question_title'] = question.title
			context['question_id'] = question_id
		elif answer_id:
			from answers.models import Answer
			answer = Answer.objects.get(pk=answer_id)
			context['question_title'] = answer.question.title
			context['question_id'] = answer.question.pk    # critical: pass question_id here
		else:
			context['question_title'] = ''
			context['question_id'] = None

		if answer_id:
			context['answer_id'] = answer_id
			context['answer_excerpt'] = answer.content[:120]
		else:
			context['answer_id'] = None
			context['answer_excerpt'] = ''

		return context



	def post(self, request, *args, **kwargs):
		# Override post to assign Generic FK fields before form.is_valid()
		self.object = None
		form = self.get_form()

		answer_id = self.kwargs.get('answer_id')
		question_id = self.kwargs.get('question_id')

		if answer_id:
			content_type = ContentType.objects.get(app_label='answers', model='answer')
			object_id = answer_id
		elif question_id:
			content_type = ContentType.objects.get(app_label='questions', model='question')
			object_id = question_id
		else:
			# Neither id provided, raise 404
			return self.handle_no_permission()

		# Set GenericForeignKey fields on form instance before validation
		form.instance.content_type = content_type
		form.instance.object_id = object_id

		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.save()
		# Always redirect to question details page
		question_id = self.kwargs.get('question_id')
		answer_id = self.kwargs.get('answer_id')

		if question_id:
			return redirect('question_details', pk=question_id)
		elif answer_id:
			answer = get_object_or_404(Answer, pk=answer_id)
			return redirect('question_details', pk=answer.question.pk)

		# fallback redirect
		return redirect('questions_list')
