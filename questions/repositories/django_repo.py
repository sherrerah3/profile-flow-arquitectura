from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .base import QuestionRepository, UserAnswerRepository
from questions.models import Question, UserQuestionAnswer


class DjangoORMQuestionRepository(QuestionRepository):
    def create_question(self, text, options):
        return Question.objects.create(text=text, options=options)

    def list_questions(self):
        return list(Question.objects.all())

    def exclude_questions(self, answered_ids):
        return Question.objects.exclude(id__in=answered_ids).first()

    def get_question(self, question_id):
        return get_object_or_404(Question, id=question_id)


class DjangoORMUserAnswerRepository(UserAnswerRepository):
    def has_answered_today(self, user):
        today = now().date()
        return UserQuestionAnswer.objects.filter(user=user, answered_at__date=today).exists()

    def get_answered_question_ids(self, user):
        return UserQuestionAnswer.objects.filter(user=user).values_list('question_id', flat=True)

    def exists_answer(self, user, question):
        return UserQuestionAnswer.objects.filter(user=user, question=question).exists()

    def create_answer(self, user, question, selected_option):
        return UserQuestionAnswer.objects.create(
            user=user,
            question=question,
            selected_option=selected_option
        )
