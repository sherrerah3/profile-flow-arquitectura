from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import QuestionSerializer

from .repositories.django_repo import DjangoORMQuestionRepository, DjangoORMUserAnswerRepository
from .services.question_service import QuestionService

class NextQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        service = QuestionService(
            DjangoORMQuestionRepository(),
            DjangoORMUserAnswerRepository()
        )

        next_question, error = service.get_next_question(user)

        if error:
            return Response({"message": error}, status=204)

        serializer = QuestionSerializer(next_question)
        return Response(serializer.data)


class AnswerQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        question_id = request.data.get("question_id")
        selected_option = request.data.get("selected_option")

        if not question_id or not selected_option:
            return Response({"error": "Faltan datos"}, status=400)

        service = QuestionService(
            DjangoORMQuestionRepository(),
            DjangoORMUserAnswerRepository()
        )

        answer, error = service.answer_question(user, question_id, selected_option)

        if error:
            return Response({"error": error}, status=400)

        return Response({"message": "Respuesta guardada"}, status=201)