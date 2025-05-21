from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now, timedelta
from .models import Question, UserQuestionAnswer
from .serializers import QuestionSerializer

class NextQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Limitar a 1 pregunta por día
        today = now().date()
        answered_today = UserQuestionAnswer.objects.filter(user=user, answered_at__date=today).exists()
        if answered_today:
            return Response({"message": "Ya respondiste la pregunta de hoy"}, status=204)

        # Aquí la lógica para filtrar la siguiente pregunta, por simplicidad:
        answered_questions = UserQuestionAnswer.objects.filter(user=user).values_list('question_id', flat=True)
        next_question = Question.objects.exclude(id__in=answered_questions).first()

        if not next_question:
            return Response({"message": "No hay más preguntas para ti."}, status=204)

        serializer = QuestionSerializer(next_question)
        return Response(serializer.data)

class AnswerQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        question_id = request.data.get('question_id')
        selected_option = request.data.get('selected_option')

        if not question_id or not selected_option:
            return Response({"error": "Faltan datos"}, status=400)

        question = get_object_or_404(Question, id=question_id)

        # Evitar duplicados
        obj, created = UserQuestionAnswer.objects.get_or_create(
            user=user,
            question=question,
            defaults={'selected_option': selected_option}
        )

        if not created:
            return Response({"error": "Ya respondiste esta pregunta"}, status=400)

        # Aquí puedes agregar lógica para filtrar vacantes basadas en respuestas, etc.

        return Response({"message": "Respuesta guardada"}, status=201)
