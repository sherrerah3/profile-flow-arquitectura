# users/auth_factory.py

from .auth_strategies import (
    AuthenticationStrategy,
    UsernamePasswordAuthStrategy,
    EmailPasswordAuthStrategy
)

class AuthStrategyFactory:
    """
    Factory para crear diferentes estrategias de autenticación.
    
    Implementa el patrón Factory Method para crear instancias de estrategias
    de autenticación basándose en el tipo solicitado.
    """
    
    # Mapeo de tipos de autenticación a sus clases correspondientes
    _strategies = {
        'username': UsernamePasswordAuthStrategy,
        'username_password': UsernamePasswordAuthStrategy,
        'email': EmailPasswordAuthStrategy,
        'email_password': EmailPasswordAuthStrategy,
    }
    
    @classmethod
    def create_strategy(cls, auth_type: str = 'username_password') -> AuthenticationStrategy:
        """
        Crea una estrategia de autenticación según el tipo especificado.
        
        Args:
            auth_type (str): Tipo de estrategia a crear.
                           Valores válidos: 'username', 'username_password', 
                           'email', 'email_password'
        
        Returns:
            AuthenticationStrategy: Instancia de la estrategia solicitada
            
        Raises:
            ValueError: Si el tipo de estrategia no está soportado
        """
        strategy_class = cls._strategies.get(auth_type.lower())
        
        if not strategy_class:
            available_strategies = ', '.join(cls._strategies.keys())
            raise ValueError(
                f"Estrategia de autenticación '{auth_type}' no soportada. "
                f"Estrategias disponibles: {available_strategies}"
            )
        
        return strategy_class()
    
    @classmethod
    def get_available_strategies(cls) -> list:
        """
        Retorna la lista de estrategias de autenticación disponibles.
        
        Returns:
            list: Lista de nombres de estrategias disponibles
        """
        return list(cls._strategies.keys())
    
    @classmethod
    def register_strategy(cls, auth_type: str, strategy_class: type):
        """
        Registra una nueva estrategia de autenticación.
        
        Permite extender el factory con nuevas estrategias sin modificar
        el código existente (Principio Abierto/Cerrado).
        
        Args:
            auth_type (str): Nombre del tipo de autenticación
            strategy_class (type): Clase que implementa AuthenticationStrategy
        
        Raises:
            TypeError: Si la clase no hereda de AuthenticationStrategy
        """
        if not issubclass(strategy_class, AuthenticationStrategy):
            raise TypeError(
                f"La clase {strategy_class.__name__} debe heredar de AuthenticationStrategy"
            )
        
        cls._strategies[auth_type.lower()] = strategy_class