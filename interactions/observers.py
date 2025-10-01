"""
Observer Pattern para el sistema de notificaciones de likes.

Este patrón permite que diferentes componentes reaccionen automáticamente
cuando ocurren eventos relacionados con likes, sin acoplamiento directo.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LikeObserver(ABC):
    """Interfaz para observadores de eventos de likes"""
    
    @abstractmethod
    def on_like_created(self, like_data: Dict[str, Any]):
        """Se ejecuta cuando se crea un like"""
        pass
    
    @abstractmethod
    def on_like_removed(self, like_data: Dict[str, Any]):
        """Se ejecuta cuando se elimina un like"""
        pass


class NotificationObserver(LikeObserver):
    """Observer que maneja notificaciones cuando hay likes"""
    
    def on_like_created(self, like_data: Dict[str, Any]):
        """Envía notificación al reclutador cuando alguien da like a su vacante"""
        user_name = like_data.get('user_name', 'Usuario')
        job_title = like_data.get('job_title', 'Vacante')
        
        notification_message = f"¡{user_name} le dio like a tu vacante '{job_title}'!"
        print(f"NOTIFICACIÓN: {notification_message}")
    
    def on_like_removed(self, like_data: Dict[str, Any]):
        """Maneja cuando se quita un like"""
        user_name = like_data.get('user_name', 'Usuario')
        job_title = like_data.get('job_title', 'Vacante')
        
        print(f"{user_name} quitó like de '{job_title}'")


class StatisticsObserver(LikeObserver):
    """Observer que actualiza estadísticas de likes"""
    
    def on_like_created(self, like_data: Dict[str, Any]):
        """Actualiza estadísticas cuando se crea un like"""
        job_id = like_data.get('job_id')
        total_likes = like_data.get('total_likes', 0)
        
        print(f"Vacante {job_id} ahora tiene {total_likes} likes")
        
        # Detectar vacantes populares
        if total_likes >= 5:
            print(f"¡Vacante {job_id} es POPULAR! ({total_likes} likes)")
    
    def on_like_removed(self, like_data: Dict[str, Any]):
        """Actualiza estadísticas cuando se quita un like"""
        job_id = like_data.get('job_id')
        total_likes = like_data.get('total_likes', 0)
        
        print(f"Vacante {job_id} ahora tiene {total_likes} likes")


class RecommendationObserver(LikeObserver):
    """Observer que invalida cache de recomendaciones cuando cambian los likes"""
    
    def on_like_created(self, like_data: Dict[str, Any]):
        """Invalida recomendaciones cuando hay nuevo like"""
        user_id = like_data.get('user_id')
        
        print(f"Actualizando recomendaciones para usuario {user_id}")
        
        # Aquí podrías integrar con tu sistema de recomendaciones
        # Por ejemplo: cache.delete(f"recommendations_user_{user_id}")
    
    def on_like_removed(self, like_data: Dict[str, Any]):
        """Invalida recomendaciones cuando se quita like"""
        user_id = like_data.get('user_id')
        
        print(f"Recalculando recomendaciones para usuario {user_id}")


class LikeSubject:
    """
    Sujeto que notifica a observadores sobre eventos de likes.
    
    Esta clase implementa el patrón Observer para manejar eventos
    relacionados con likes de forma desacoplada.
    """
    
    def __init__(self):
        self._observers: List[LikeObserver] = []
    
    def attach(self, observer: LikeObserver):
        """Registra un observador"""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"Observer {observer.__class__.__name__} registrado")
    
    def detach(self, observer: LikeObserver):
        """Remueve un observador"""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"Observer {observer.__class__.__name__} removido")
    
    def notify_like_created(self, like_data: Dict[str, Any]):
        """Notifica a todos los observadores sobre un nuevo like"""
        for observer in self._observers:
            try:
                observer.on_like_created(like_data)
            except Exception as e:
                print(f"Error en observer {observer.__class__.__name__}: {e}")
    
    def notify_like_removed(self, like_data: Dict[str, Any]):
        """Notifica a todos los observadores sobre un like removido"""
        for observer in self._observers:
            try:
                observer.on_like_removed(like_data)
            except Exception as e:
                print(f"Error en observer {observer.__class__.__name__}: {e}")


# Instancia global del sujeto (Singleton pattern implícito)
like_subject = LikeSubject()

# Registrar observadores por defecto
like_subject.attach(NotificationObserver())
like_subject.attach(StatisticsObserver())
like_subject.attach(RecommendationObserver())


def get_like_subject() -> LikeSubject:
    """Obtiene la instancia global del sujeto de likes"""
    return like_subject