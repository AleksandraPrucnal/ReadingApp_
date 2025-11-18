from uuid import UUID
from src.infrastructure.repositories.progress_repository import ProgressRepository
from src.infrastructure.dto.progressDTO import UserProgressDTO, ChartPointDTO


class ProgressService:
    def __init__(self, repository: ProgressRepository):
        self._repository = repository

    def _calculate_level_info(self, total_points: int) -> tuple[int, int, int]:
        """
        Logika levelowania 1-5.
        Zwraca: (obecny_level, próg_następnego, ile_brakuje)
        """
        # Progi punktowe (możesz zmienić te liczby)
        # Level 1: 0-100
        # Level 2: 101-300
        # Level 3: 301-600
        # Level 4: 601-1000
        # Level 5: 1000+
        levels = {
            1: 100,
            2: 300,
            3: 600,
            4: 1000,
            5: 999999  # Max level
        }

        current_level = 1
        next_threshold = levels[1]

        for lvl, threshold in levels.items():
            if total_points >= threshold:
                # Jeśli mamy więcej punktów niż próg, wchodzimy na wyższy level (do max 5)
                if lvl < 5:
                    current_level = lvl + 1
                    next_threshold = levels[lvl + 1]
                else:
                    current_level = 5
                    next_threshold = total_points  # Już nie rośnie
            else:
                # Nie osiągnęliśmy progu tego levelu, więc zostajemy na poprzednim (lub 1)
                # Pętla logiczna tutaj zapewnia poprawne wyliczenie
                break

        # Fix logiczny dla prostych progów:
        # Jeśli total=50 (lvl 1), next=100.
        # Jeśli total=150 (lvl 2), next=300.
        if total_points < levels[1]:
            current_level = 1
            next_threshold = levels[1]
        elif total_points < levels[2]:
            current_level = 2
            next_threshold = levels[2]
        elif total_points < levels[3]:
            current_level = 3
            next_threshold = levels[3]
        elif total_points < levels[4]:
            current_level = 4
            next_threshold = levels[4]
        else:
            current_level = 5
            next_threshold = total_points

        points_to_next = next_threshold - total_points
        if points_to_next < 0: points_to_next = 0

        return current_level, next_threshold, points_to_next

    async def get_user_stats(self, user_id: UUID) -> UserProgressDTO:
        # 1. Pobierz historię z bazy
        raw_history = await self._repository.get_user_history(user_id)

        # 2. Oblicz sumę punktów i przygotuj dane do wykresu
        total_points = 0
        chart_history = []

        for row in raw_history:
            points = row['rate']
            total_points += points

            # Formatujemy datę do stringa (np. "2023-11-18")
            date_str = row['completed_at'].strftime("%Y-%m-%d")

            chart_history.append(ChartPointDTO(
                date=date_str,
                points=points
            ))

        # 3. Oblicz level
        lvl, threshold, missing = self._calculate_level_info(total_points)

        return UserProgressDTO(
            total_points=total_points,
            current_level=lvl,
            next_level_threshold=threshold,
            points_to_next_level=missing,
            history=chart_history
        )