from src.db import database
from src.db import progress_table
from src.core.domain.progress import ProgressIn


class ProgressRepository:
    async def add_progress(self, data: ProgressIn) -> None:
        # 1. Zamieniamy model Pydantic na słownik
        values = data.model_dump()

        # 2. Mapujemy 'id_exercise' (z modelu Pydantic) na 'exercise_id' (z bazy danych)
        # Model ProgressIn ma pole 'id_exercise', a tabela w bazie ma 'exercise_id'.
        if 'id_exercise' in values:
            values['exercise_id'] = values.pop('id_exercise')

        # 3. Wstawiamy do bazy używając poprawionego słownika
        query = progress_table.insert().values(**values)
        await database.execute(query)