# utils.py
from answers.models import Answer
from comments.models import Comment
from questions.models import Question


def get_root_question(obj):
	"""
	Walks up the chain from a Question/Answer/Comment to find the root Question.
	"""
	while True:
		if isinstance(obj, Question):
			return obj
		if isinstance(obj, Answer):
			return obj.question
		if isinstance(obj, Comment):
			obj = obj.content_object
		else:
			return None

def get_comment_context(kwargs):
	"""
	Extract context data for templates from URL kwargs:
	Supports question_id, answer_id, comment_id or parent_comment_id.
	"""
	question = None
	answer = None
	parent_comment = None

	question_id = kwargs.get('question_id')
	answer_id = kwargs.get('answer_id')
	comment_id = kwargs.get('comment_id') or kwargs.get('parent_comment_id')

	if question_id:
		question = Question.objects.filter(pk=question_id).first()

	elif answer_id:
		answer = Answer.objects.filter(pk=answer_id).first()
		question = answer.question if answer else None

	elif comment_id:
		# This is the immediate parent comment ID
		parent_comment = Comment.objects.filter(pk=comment_id).first()
		if parent_comment:
			# find root question for context title, but keep parent_comment separately
			question = get_root_question(parent_comment.content_object)

	context = {
		'question_title': question.title if question else '',
		'question_id': question.pk if question else None,
		'answer_id': answer_id if answer_id else None,
		'answer_excerpt': getattr(answer, 'content', '')[:120] if answer_id else '',
		'parent_comment': parent_comment,  # keep the actual comment object, not its content_object
		'exists': False,  # default this; views override as needed
	}
	return context

