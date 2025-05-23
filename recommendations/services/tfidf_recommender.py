from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jobs.models import Job
from interactions.models import Interaction
from .base_recommender import BaseRecommender


class TFIDFRecommender(BaseRecommender):

    def obtener_corpus(self, user):
        todas_las_vacantes = Job.objects.all()

        def job_to_text(job):
            return " ".join([
                str(job.title),
                str(job.description),
                " ".join([kw.strip() for kw in str(job.keywords).split(",") if kw.strip()])
            ])

        textos_vacantes = [job_to_text(job) for job in todas_las_vacantes]

        # Filtra solo vacantes con "like", no solo vistas
        vacantes_interes_usuario = Job.objects.filter(
            interactions__user=user,
            interactions__interaction_type='like'
        ).distinct()

        texto_usuario = " ".join([job_to_text(job) for job in vacantes_interes_usuario])

        return textos_vacantes, texto_usuario, todas_las_vacantes

    def vectorizar(self, textos):
        vectorizer = TfidfVectorizer(stop_words="english")
        return vectorizer.fit_transform(textos)

    def calcular_similitud(self, matriz):
        return cosine_similarity(matriz[-1], matriz[:-1]).flatten()

    def seleccionar(self, similitudes, objetos, top_n):
        # Filtra vacantes ya vistas o con like
        vacantes_vistas_ids = set(
            Interaction.objects.filter(user=self.usuario).values_list("job_id", flat=True)
        )

        recomendaciones = [
            obj for i, obj in sorted(
                enumerate(objetos), key=lambda x: similitudes[x[0]], reverse=True
            )
            if obj.id not in vacantes_vistas_ids
        ]

        return recomendaciones[:min(len(recomendaciones), top_n)]


# Función de ayuda externa
def recomendar_vacantes(user, top_n=5):
    recomendador = TFIDFRecommender()
    return recomendador.recomendar(user, top_n)
