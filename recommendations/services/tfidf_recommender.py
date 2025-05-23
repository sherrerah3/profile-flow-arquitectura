from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from jobs.models import Job
from interactions.models import Interaction


def obtener_corpus_para_usuario(user):
    todas_las_vacantes = Job.objects.all()

    textos_vacantes = [f"{job.title} {job.description} {job.keywords}" for job in todas_las_vacantes]

    vacantes_interes_usuario = Job.objects.filter(interactions__user=user).distinct()

    texto_usuario = " ".join([
        f"{job.title} {job.description} {job.keywords}"
        for job in vacantes_interes_usuario
    ])

    return textos_vacantes, texto_usuario, todas_las_vacantes


def recomendar_vacantes(user, top_n=5):
    textos_vacantes, texto_usuario, vacantes = obtener_corpus_para_usuario(user)

    if not texto_usuario.strip():
        return []  # Si no hay likes o vistas, no se puede recomendar

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(textos_vacantes + [texto_usuario])

    similitudes = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

    top_indices = similitudes.argsort()[-top_n:][::-1]

    vacantes_list = list(vacantes)
    vacantes_recomendadas = [vacantes_list[int(i)] for i in top_indices]


    return vacantes_recomendadas
