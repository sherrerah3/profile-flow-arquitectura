class QuestionService:
    def __init__(self, question_repo, user_answer_repo):
        self.question_repo = question_repo
        self.user_answer_repo = user_answer_repo

    def get_next_question(self, user):
        if self.user_answer_repo.has_answered_today(user):
            return None, "Ya respondiste la pregunta de hoy"

        answered_ids = self.user_answer_repo.get_answered_question_ids(user)
        next_question = self.question_repo.exclude_questions(answered_ids)

        if not next_question:
            return None, "No hay más preguntas para ti."

        return next_question, None

    def answer_question(self, user, question_id, selected_option):
        question = self.question_repo.get_question(question_id)

        if self.user_answer_repo.exists_answer(user, question):
            return None, "Ya respondiste esta pregunta"

        answer = self.user_answer_repo.create_answer(user, question, selected_option)
        return answer, None
