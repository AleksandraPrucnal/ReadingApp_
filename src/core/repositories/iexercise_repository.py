from abc import ABC, abstractmethod
from typing import Optional, Union, Any, Iterable, Sequence

from src.core.domain.enums import ExerciseType
from src.core.domain.exercises.exercise_base import Exercise, ExerciseIn
from src.core.domain.exercises.exercise_match import ExerciseMatchIn
from src.core.domain.exercises.exercise_question import ExerciseQuestionIn
from src.core.domain.exercises.question import Question, QuestionIn


class IExerciseRepository(ABC):

    @abstractmethod
    async def get_all_exercises(self, *, limit: int = 50, offset: int = 0) -> Iterable[Any]:
        """
        Zwraca listę ćwiczeń (bazowy Exercise: id_exercise, type, level, topics).
        Nie ładuje ciężkich pól (tekst, obrazki, pytania).
        """
        pass

    @abstractmethod
    async def get_by_id(self, id_exercise: int) -> Any | None:
        """
        Zwraca ExerciseMatch lub ExerciseQuestion, w zależności od typu.
        """
        pass

    @abstractmethod
    async def get_by_level(self, level: int, *, limit: int = 50, offset: int = 0) -> Iterable[Any]:
        """Lista ćwiczeń o danym poziomie trudności."""
        pass

    @abstractmethod
    async def get_by_type(self, type_: ExerciseType, *, limit: int = 50, offset: int = 0) -> Iterable[Any]:
        """Lista ćwiczeń po typie."""
        pass

    @abstractmethod
    async def get_by_topics(
        self,
        topic_ids: Sequence[int],
        *,
        match_all: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> Iterable[Any]:
        """
        Lista ćwiczeń po tematach.
        match_all=False -> OR (ćwiczenie ma dowolny z topiców)
        match_all=True  -> AND (ćwiczenie ma wszystkie podane topiki)
        """
        pass

    @abstractmethod
    async def list_questions(self, id_exercise: int) -> Iterable[Any]:
        """
        Zwraca pytania powiązane z ćwiczeniem question (pusta lista dla match lub gdy brak).
        """
        pass

    @abstractmethod
    async def get_question(self, id_question: int) -> Any:
        """Zwraca pytanie po id_question."""
        pass

    @abstractmethod
    async def add_exercise_match(self, data: ExerciseMatchIn) -> Any | None:
        """Utwórz ćwiczenie typu match."""
        pass

    @abstractmethod
    async def add_exercise_question(self, data: ExerciseQuestionIn) -> Any | None:
        """Utwórz pytanie."""
        pass

    @abstractmethod
    async def add_question(self, id_exercise: int, data: QuestionIn) -> Any | None:
        """
        Dodaj pojedyncze pytanie do ćwiczenia question.
        Implementacja powinna rzucić wyjątek, jeśli id_exercise nie jest typu question.
        """
        pass

    @abstractmethod
    async def update_exercise_match(self, id_exercise: int, data: ExerciseMatchIn) -> Any | None:
        """
        Pełny update ćwiczenia (match) zgodnie z dostarczonym typem danych.
        """
        pass

    @abstractmethod
    async def update_exercise_question(self, id_exercise: int, data: ExerciseQuestionIn) -> Any | None:
        """
        Pełny update ćwiczenia (question) zgodnie z dostarczonym typem danych.
        """
        pass

    @abstractmethod
    async def update_question(self, id_question: int, data: QuestionIn) -> Any | None:
        """Zaktualizuj pytanie."""
        pass

    @abstractmethod
    async def delete_exercise(self, id_exercise: int) -> bool:
        """Usuń ćwiczenie (match lub question)."""
        pass

    @abstractmethod
    async def delete_question(self, id_question: int) -> bool:
        """Usuń pytanie. True, jeśli istniało i zostało usunięte."""
        pass

    @abstractmethod
    async def check_answer_match(
            self,
            id_exercise: int,
            selected_index: int
    ) -> tuple[int, bool]:
        """Sprawdza czy podana odpowiedz jest poprawna.
        Przyjmuje id_exercise oraz indeks wybranej odpowiedzi.
        Jesli indeks jest taki sam jak indeks poprawnej odpowiedzi -> wyrzuca [id_exercise,True]
        W innym przypadku wyrzuca [id_exercise,False]"""
        pass

    @abstractmethod
    async def check_answer_question_single(
            self,
            id_exercise: int,
            id_question: int,
            selected_index: int,
    ) -> tuple[int, int, bool]:
        """Sprawdza czy podana odpowiedz do
        wybranego cwiczenia i wybranego pytania jest poprawna."""
        pass