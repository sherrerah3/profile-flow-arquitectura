class BaseRecommender:
    def recomendar(self, user, top_n=5):
        self.usuario = user  # NUEVO: para usarlo en seleccionar
        textos, texto_usuario, objetos = self.obtener_corpus(user)
        if not texto_usuario.strip():
            return []

        matriz = self.vectorizar(textos + [texto_usuario])
        similitudes = self.calcular_similitud(matriz)
        return self.seleccionar(similitudes, objetos, top_n)

    def obtener_corpus(self, user):
        raise NotImplementedError("Debes implementar 'obtener_corpus'")

    def vectorizar(self, textos):
        raise NotImplementedError("Debes implementar 'vectorizar'")

    def calcular_similitud(self, matriz):
        raise NotImplementedError("Debes implementar 'calcular_similitud'")

    def seleccionar(self, similitudes, objetos, top_n):
<<<<<<< HEAD
        raise NotImplementedError("Debes implementar 'seleccionar'")
=======
        raise NotImplementedError("Debes implementar 'seleccionar'")
>>>>>>> Samuel
