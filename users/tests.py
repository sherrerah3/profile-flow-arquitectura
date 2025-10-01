from django.test import TestCase
from .auth_factory import AuthStrategyFactory
from .auth_strategies import UsernamePasswordAuthStrategy, EmailPasswordAuthStrategy

class FactoryPatternTest(TestCase):
    """Test básico para demostrar que el Factory Pattern funciona"""
    
    def test_factory_creates_strategies(self):
        """Test: Factory crea las estrategias correctamente"""
        username_strategy = AuthStrategyFactory.create_strategy('username')
        email_strategy = AuthStrategyFactory.create_strategy('email')
        
        self.assertIsInstance(username_strategy, UsernamePasswordAuthStrategy)
        self.assertIsInstance(email_strategy, EmailPasswordAuthStrategy)
    
    def test_factory_handles_invalid_strategy(self):
        """Test: Factory maneja estrategias inválidas"""
        with self.assertRaises(ValueError):
            AuthStrategyFactory.create_strategy('invalid')
