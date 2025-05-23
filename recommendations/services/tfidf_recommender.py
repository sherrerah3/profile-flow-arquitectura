from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from jobs.models import Job
from interactions.models import Interaction
from .base_recommender import BaseRecommender


class TFIDFRecommender(BaseRecommender):

    def recomendar(self, user, top_n=5):
        self.user = user  # guardamos el usuario en el objeto
        textos, texto_usuario, objetos = self.obtener_corpus(user)
        if not texto_usuario.strip():
            return []

        matriz = self.vectorizar(textos + [texto_usuario])
        similitudes = self.calcular_similitud(matriz)
        return self.seleccionar(similitudes, objetos, top_n)

    def obtener_corpus(self, user):
        todas_las_vacantes = Job.objects.all()

        def job_to_text(job):
            return " ".join([
                str(job.title),
                str(job.description),
                " ".join([kw.strip() for kw in str(job.keywords).split(",") if kw.strip()])
            ])

        textos_vacantes = [job_to_text(job) for job in todas_las_vacantes]

        vacantes_interes_usuario = Job.objects.filter(
            interactions__user=user,
            interactions__interaction_type='like'
        ).distinct()

        texto_usuario = " ".join([job_to_text(job) for job in vacantes_interes_usuario])

        return textos_vacantes, texto_usuario, list(todas_las_vacantes)

    def vectorizar(self, textos):
        vectorizer = TfidfVectorizer(stop_words="english")
        return vectorizer.fit_transform(textos)

    def calcular_similitud(self, matriz):
        return cosine_similarity(matriz[-1], matriz[:-1]).flatten()

    def seleccionar(self, similitudes, objetos, top_n):
        # IDs de vacantes ya vistas o con like
        vacantes_vistas_ids = set(
            Interaction.objects.filter(user=self.user).values_list("job_id", flat=True)
        )

        # Asociar cada vacante con su similitud
        vacantes_con_similitud = [
            (obj, similitud)
            for obj, similitud in zip(objetos, similitudes)
            if obj.id not in vacantes_vistas_ids
        ]

        # Ordenar por similitud descendente
        vacantes_ordenadas = sorted(vacantes_con_similitud, key=lambda x: x[1], reverse=True)

        # Retornar top_n con similitud
        return [
            self.agregar_similitud(obj, sim)
            for obj, sim in vacantes_ordenadas[:top_n]
        ]

    def agregar_similitud(self, job, similitud):
        job.similarity = round(float(similitud), 4)
        return job


# Función externa
def recomendar_vacantes(user, top_n=5):
    recomendador = TFIDFRecommender()
<<<<<<< HEAD
    return recomendador.recomendar(user, top_n)
=======
    return recomendador.recomendar(user, top_n)
>>>>>>> Samuel
