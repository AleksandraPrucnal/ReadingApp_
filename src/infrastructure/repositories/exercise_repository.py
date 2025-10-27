from typing import Any, Iterable, Sequence, List, Dict
from sqlalchemy import select
from src.core.domain.enums import ExerciseType
from src.core.domain.exercises.exercise_match import ExerciseMatchIn
from src.core.domain.exercises.exercise_question import ExerciseQuestionIn
from src.core.domain.exercises.question import QuestionIn
from src.infrastructure.dto.exerciseDTO import (
    ExerciseMatchDTO,
    ExerciseQuestionDTO,
    QuestionDTO,
)
from src.db import (
    database,
    exercise_table,
    exercise_match_table,
    exercise_question_table,
    question_table,
)


class ExerciseRepository:

    async def _hydrate_many(self, base_rows: List[Dict[str, Any]]) -> List[Any]:
        if not base_rows:
            return []


        match_ids = [r["id_exercise"] for r in base_rows if ExerciseType(r["type"]) == ExerciseType.MATCH]
        question_ids = [r["id_exercise"] for r in base_rows if ExerciseType(r["type"]) == ExerciseType.QUESTION]

        match_rows = []
        if match_ids:
            match_rows = await database.fetch_all(
                select(
                    exercise_match_table.c.exercise_id,
                    exercise_match_table.c.text,
                    exercise_match_table.c.image_urls,
                    exercise_match_table.c.correct_index,
                ).where(exercise_match_table.c.exercise_id.in_(match_ids))
            )
        match_map = {r["exercise_id"]: dict(r) for r in match_rows}

        question_rows = []
        if question_ids:
            question_rows = await database.fetch_all(
                select(
                    exercise_question_table.c.exercise_id,
                    exercise_question_table.c.text,
                    exercise_question_table.c.image_url,
                ).where(exercise_question_table.c.exercise_id.in_(question_ids))
            )
        question_map = {r["exercise_id"]: dict(r) for r in question_rows}

        out: List[Any] = []
        for b in base_rows:
            ex_type = ExerciseType(b["type"])
            if ex_type == ExerciseType.MATCH:
                det = match_map.get(b["id_exercise"])
                if not det:
                    continue
                record = {
                    "id_exercise": b["id_exercise"],
                    "type": b["type"],
                    "level": b["level"],
                    "topics": b.get("topics") or [],
                    "text": det["text"],
                    "image_urls": list(det.get("image_urls") or []),
                    "correct_index": det["correct_index"],
                }
                out.append(ExerciseMatchDTO.from_record(record))
            else:
                det = question_map.get(b["id_exercise"])
                if not det:
                    continue
                record = {
                    "id_exercise": b["id_exercise"],
                    "type": b["type"],
                    "level": b["level"],
                    "topics": b.get("topics") or [],
                    "text": det["text"],
                    "image_url": det.get("image_url") or "",
                }
                out.append(ExerciseQuestionDTO.from_record(record))
        return out

    # ================= Reads (kolekcje) =================

    async def get_all_exercises(self, *, limit: int = 50, offset: int = 0) -> Iterable[Any]:
        rows = await database.fetch_all(
            select(
                exercise_table.c.id_exercise,
                exercise_table.c.type,
                exercise_table.c.level,
                exercise_table.c.topics,
            )
            .order_by(exercise_table.c.id_exercise)
            .limit(limit)
            .offset(offset)
        )
        return await self._hydrate_many([dict(r) for r in rows])

    async def get_by_level(self, level: int, *, limit: int = 50, offset: int = 0) -> Iterable[Any]:
        rows = await database.fetch_all(
            select(
                exercise_table.c.id_exercise,
                exercise_table.c.type,
                exercise_table.c.level,
                exercise_table.c.topics,
            )
            .where(exercise_table.c.level == level)
            .order_by(exercise_table.c.id_exercise)
            .limit(limit)
            .offset(offset)
        )
        return await self._hydrate_many([dict(r) for r in rows])

    async def get_by_type(self, type_: ExerciseType, *, limit: int = 50, offset: int = 0) -> Iterable[Any]:
        rows = await database.fetch_all(
            select(
                exercise_table.c.id_exercise,
                exercise_table.c.type,
                exercise_table.c.level,
                exercise_table.c.topics,
            )
            .where(exercise_table.c.type == type_.value)
            .order_by(exercise_table.c.id_exercise)
            .limit(limit)
            .offset(offset)
        )
        return await self._hydrate_many([dict(r) for r in rows])

    async def get_by_topics(
        self,
        topic_ids: Sequence[int],
        *,
        match_all: bool = False,
        limit: int = 50,
        offset: int = 0,
    ) -> Iterable[Any]:
        if not topic_ids:
            return await self.get_all_exercises(limit=limit, offset=offset)

        rows = await database.fetch_all(
            select(
                exercise_table.c.id_exercise,
                exercise_table.c.type,
                exercise_table.c.level,
                exercise_table.c.topics,
            )
            .order_by(exercise_table.c.id_exercise)
            .limit(10000)
        )
        wanted = set(topic_ids)
        filtered: List[Dict[str, Any]] = []
        for r in rows:
            ts = set((r["topics"] or []))
            if match_all:
                if wanted.issubset(ts):
                    filtered.append(dict(r))
            else:
                if ts.intersection(wanted):
                    filtered.append(dict(r))
        base_rows = filtered[offset : offset + limit]
        return await self._hydrate_many(base_rows)

    # ================= Questions (read) =================

    async def list_questions(self, id_exercise: int) -> Iterable[QuestionDTO]:
        rows = await database.fetch_all(
            select(question_table)
            .where(question_table.c.exercise_id == id_exercise)
            .order_by(question_table.c.id_question)
        )
        return [QuestionDTO(**dict(r)) for r in rows]

    async def get_question(self, id_question: int) -> QuestionDTO | None:
        r = await database.fetch_one(
            select(question_table).where(question_table.c.id_question == id_question)
        )
        return QuestionDTO(**dict(r)) if r else None

    # ================= Creates =================

    async def _insert_exercise(self, type_: ExerciseType, level: int, topics: list[int]) -> int:
        return await database.execute(
            exercise_table.insert().values(
                type=type_.value,
                level=level,
                topics=list(topics or []),
            )
        )

    async def add_exercise_match(self, data: ExerciseMatchIn) -> Any | None:
        async with database.transaction():
            ex_id = await self._insert_exercise(data.type, data.level, data.topics)
            await database.execute(
                exercise_match_table.insert().values(
                    exercise_id=ex_id,
                    text=data.text,
                    image_urls=list(data.image_urls or []),
                    correct_index=data.correct_index,
                )
            )
        return await self._get_match_by_id(ex_id)

    async def add_exercise_question(self, data: ExerciseQuestionIn) -> Any | None:
        async with database.transaction():
            ex_id = await self._insert_exercise(data.type, data.level, data.topics)
            await database.execute(
                exercise_question_table.insert().values(
                    exercise_id=ex_id,
                    text=data.text,
                    image_url=data.image_url,
                )
            )
        return await self._get_question_by_id(ex_id)

    async def add_question(self, id_exercise: int, data: QuestionIn) -> Any | None:
        """
        Dodaje pytanie do ćwiczenia typu 'text_question'.
        Zwraca słownik z nowo utworzonym pytaniem (pasuje do QuestionDTO).
        """
        base = await database.fetch_one(
            select(exercise_table.c.type).where(exercise_table.c.id_exercise == id_exercise)
        )
        if not base or ExerciseType(base["type"]) != ExerciseType.QUESTION:
            raise ValueError("Cannot add question to a non-question exercise.")

        new_id = await database.execute(
            question_table.insert().values(
                exercise_id=id_exercise,
                question=data.question,
                answers=list(data.answers or []),
                correct_index=data.correct_index,
            )
        )

        row = await database.fetch_one(
            select(question_table).where(question_table.c.id_question == new_id)
        )
        return dict(row) if row else None

    # ================= Reads (po ID) =================
    async def get_by_id(self, id_exercise: int) -> Any | None:
        """Zwraca pojedyncze ćwiczenie (MATCH lub QUESTION) po ID."""
        base = await database.fetch_one(
            select(exercise_table.c.type).where(exercise_table.c.id_exercise == id_exercise)
        )
        if not base:
            return None

        ex_type = ExerciseType(base["type"])
        if ex_type == ExerciseType.MATCH:
            return await self._get_match_by_id(id_exercise)
        elif ex_type == ExerciseType.QUESTION:
            return await self._get_question_by_id(id_exercise)
        return None

    async def _get_match_by_id(self, id_exercise: int) -> Any | None:
        base = await database.fetch_one(
            select(exercise_table).where(exercise_table.c.id_exercise == id_exercise)
        )
        details = await database.fetch_one(
            select(exercise_match_table).where(exercise_match_table.c.exercise_id == id_exercise)
        )
        if not base or not details:
            return None

        record = {
            "id_exercise": base["id_exercise"],
            "type": base["type"],
            "level": base["level"],
            "topics": list((base["topics"] or [])),
            "text": details["text"],
            "image_urls": list((details["image_urls"] or [])),
            "correct_index": details["correct_index"],
        }
        return ExerciseMatchDTO.from_record(record)

    """
    async def _get_question_by_id(self, id_exercise: int) -> Any | None:
        base = await database.fetch_one(
            select(exercise_table).where(exercise_table.c.id_exercise == id_exercise)
        )
        details = await database.fetch_one(
            select(exercise_question_table).where(exercise_question_table.c.exercise_id == id_exercise)
        )
        if not base or not details:
            return None

        b = dict(base)
        d = dict(details)

        record = {
            "id_exercise": b["id_exercise"],
            "type": b["type"],  # 'text_question'
            "level": b["level"],
            "topics": list(b.get("topics") or []),
            "text": d["text"],
            "image_url": d.get("image_url") or "",
            "questions": [],  
        }
        return ExerciseQuestionDTO.from_record(record)
    """

    async def _get_question_by_id(self, id_exercise: int) -> Any | None:
        base_rec = await database.fetch_one(
            select(exercise_table).where(exercise_table.c.id_exercise == id_exercise)
        )
        details_rec = await database.fetch_one(
            select(exercise_question_table).where(exercise_question_table.c.exercise_id == id_exercise)
        )
        if not base_rec or not details_rec:
            return None

        base = dict(base_rec)
        details = dict(details_rec)

        qs_rows = await database.fetch_all(
            select(
                question_table.c.id_question,
                question_table.c.question,
                question_table.c.answers,
                question_table.c.correct_index,
            )
            .where(question_table.c.exercise_id == id_exercise)
            .order_by(question_table.c.id_question)
        )
        questions = [dict(r) for r in qs_rows]

        record = {
            "id_exercise": base["id_exercise"],
            "type": base["type"],  # "text_question"
            "level": base["level"],
            "topics": base.get("topics") or [],
            "text": details["text"],
            "image_url": details.get("image_url") or "",
            "questions": questions,
        }
        return ExerciseQuestionDTO.from_record(record)

    # ================= Updates =================

    async def update_exercise_match(self, id_exercise: int, data: ExerciseMatchIn) -> Any | None:
        base = await database.fetch_one(
            select(exercise_table.c.type).where(exercise_table.c.id_exercise == id_exercise)
        )
        if not base or ExerciseType(base["type"]) != ExerciseType.MATCH:
            return None

        async with database.transaction():
            await database.execute(
                exercise_table.update()
                .where(exercise_table.c.id_exercise == id_exercise)
                .values(level=data.level, topics=list(data.topics or []))
            )
            await database.execute(
                exercise_match_table.update()
                .where(exercise_match_table.c.exercise_id == id_exercise)
                .values(
                    text=data.text,
                    image_urls=list(data.image_urls or []),
                    correct_index=data.correct_index,
                )
            )
        return await self._get_match_by_id(id_exercise)

    async def update_exercise_question(self, id_exercise: int, data: ExerciseQuestionIn) -> Any | None:
        base = await database.fetch_one(
            select(exercise_table.c.type).where(exercise_table.c.id_exercise == id_exercise)
        )
        if not base or ExerciseType(base["type"]) != ExerciseType.QUESTION:
            return None

        async with database.transaction():
            await database.execute(
                exercise_table.update()
                .where(exercise_table.c.id_exercise == id_exercise)
                .values(level=data.level, topics=list(data.topics or []))
            )
            await database.execute(
                exercise_question_table.update()
                .where(exercise_question_table.c.exercise_id == id_exercise)
                .values(text=data.text, image_url=data.image_url)
            )
        return await self._get_question_by_id(id_exercise)

    async def update_question(self, id_question: int, data: QuestionIn) -> Any | None:
        exists = await database.fetch_one(
            select(question_table.c.id_question).where(question_table.c.id_question == id_question)
        )
        if not exists:
            return None

        await database.execute(
            question_table.update()
            .where(question_table.c.id_question == id_question)
            .values(
                question=data.question,
                answers=list(data.answers or []),
                correct_index=data.correct_index,
            )
        )
        row = await database.fetch_one(
            select(question_table).where(question_table.c.id_question == id_question)
        )
        return QuestionDTO(**dict(row)) if row else None

    # ================= Deletes =================

    async def delete_exercise(self, id_exercise: int) -> bool:
        base = await database.fetch_one(
            select(exercise_table.c.type).where(exercise_table.c.id_exercise == id_exercise)
        )
        if not base:
            return False
        ex_type = ExerciseType(base["type"])

        async with database.transaction():
            if ex_type == ExerciseType.MATCH:
                await database.execute(
                    exercise_match_table.delete()
                    .where(exercise_match_table.c.exercise_id == id_exercise)
                )
            else:
                await database.execute(
                    question_table.delete()
                    .where(question_table.c.exercise_id == id_exercise)
                )
                await database.execute(
                    exercise_question_table.delete()
                    .where(exercise_question_table.c.exercise_id == id_exercise)
                )
            await database.execute(
                exercise_table.delete().where(exercise_table.c.id_exercise == id_exercise)
            )
        return True

    async def delete_question(self, id_question: int) -> bool:
        exists = await database.fetch_one(
            select(question_table.c.id_question).where(question_table.c.id_question == id_question)
        )
        if not exists:
            return False
        await database.execute(
            question_table.delete().where(question_table.c.id_question == id_question)
        )
        return True

    # ================= Answer checking =================

    async def check_answer_match(self, id_exercise: int, selected_index: int) -> tuple[int, bool]:
        base = await database.fetch_one(
            select(exercise_table.c.type).where(exercise_table.c.id_exercise == id_exercise)
        )
        if not base:
            raise ValueError("Exercise not found")
        if ExerciseType(base["type"]) != ExerciseType.MATCH:
            raise ValueError("Exercise is not of type match_image")

        det = await database.fetch_one(
            select(
                exercise_match_table.c.correct_index,
                exercise_match_table.c.image_urls,
            ).where(exercise_match_table.c.exercise_id == id_exercise)
        )
        if not det:
            return (id_exercise, False)

        urls = det["image_urls"] or []
        if not (0 <= selected_index < len(urls)):
            return (id_exercise, False)

        return (id_exercise, selected_index == det["correct_index"])

    async def check_answer_question_single(
        self,
        id_exercise: int,
        id_question: int,
        selected_index: int,
    ) -> tuple[int, int, bool]:
        base = await database.fetch_one(
            select(exercise_table.c.type).where(exercise_table.c.id_exercise == id_exercise)
        )
        if not base:
            raise ValueError("Exercise not found")
        if ExerciseType(base["type"]) != ExerciseType.QUESTION:
            raise ValueError("Exercise is not of type text_question")

        row = await database.fetch_one(
            select(question_table.c.correct_index, question_table.c.answers)
            .where(question_table.c.id_question == id_question)
            .where(question_table.c.exercise_id == id_exercise)
        )
        if not row:
            return (id_exercise, id_question, False)

        answers = row["answers"] or []
        if not (0 <= selected_index < len(answers)):
            return (id_exercise, id_question, False)

        return (id_exercise, id_question, selected_index == row["correct_index"])
