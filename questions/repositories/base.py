from abc import ABC, abstractmethod
from typing import List, Optional, Any


class QuestionRepository(ABC):
    @abstractmethod
    def create_question(self, text: str, options: List[str]) -> Any:
        pass

    @abstractmethod
    def list_questions(self) -> List[Any]:
        pass

    @abstractmethod
    def exclude_questions(self, answered_ids: List[int]) -> Optional[Any]:
        """Devuelve la siguiente pregunta que no esté en answered_ids o None"""
        pass

    @abstractmethod
    def get_question(self, question_id: int) -> Any:
        pass


class UserAnswerRepository(ABC):
    @abstractmethod
    def has_answered_today(self, user) -> bool:
        pass

    @abstractmethod
    def get_answered_question_ids(self, user) -> List[int]:
        pass

    @abstractmethod
    def exists_answer(self, user, question) -> bool:
        pass

    @abstractmethod
    def create_answer(self, user, question, selected_option) -> Any:
        pass
