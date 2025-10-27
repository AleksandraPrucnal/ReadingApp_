from typing import List, Union, Annotated, Literal
from asyncpg import Record  # type: ignore
from pydantic import BaseModel, ConfigDict, Field
from src.core.domain.enums import ExerciseType


class QuestionDTO(BaseModel):
    id_question: int
    question: str
    answers: List[str]
    correct_index: int
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class _ExerciseCommon(BaseModel):
    id_exercise: int
    level: int
    # po uproszczeniu: topics trzymamy w kolumnie ARRAY(INT) w tabeli exercises
    topics: List[int] = []
    model_config = ConfigDict(from_attributes=True, extra="ignore")


class ExerciseMatchDTO(_ExerciseCommon):
    # dokładnie ma być 'match_image'
    type: Literal["match_image"]
    text: str
    image_urls: List[str]
    correct_index: int

    @classmethod
    def from_record(cls, record: Record) -> "ExerciseMatchDTO":
        r = dict(record)

        # zapewnijmy, że type ma DOSŁOWNIE 'match_image'
        typ = r.get("type")
        if isinstance(typ, ExerciseType):
            typ = typ.value  # 'match_image'
        else:
            typ = str(typ)
        # UWAGA: NIE rób str(ExerciseType.MATCH) -> to da 'ExerciseType.MATCH'

        return cls(
            id_exercise=r["id_exercise"],
            type=typ,  # 'match_image'
            level=r["level"],
            topics=list(r.get("topics") or []),
            text=r["text"],  # <-- wcześniej brakowało, stąd ValidationError
            image_urls=list(r.get("image_urls") or []),
            correct_index=r["correct_index"],
        )


class ExerciseQuestionDTO(_ExerciseCommon):
    # dokładnie ma być 'text_question'
    type: Literal["text_question"]
    text: str
    image_url: str
    questions: List[QuestionDTO] = []

    @classmethod
    def from_record(cls, record: Record) -> "ExerciseQuestionDTO":
        r = dict(record)

        typ = r.get("type")
        if isinstance(typ, ExerciseType):
            typ = typ.value  # 'text_question'
        else:
            typ = str(typ)

        return cls(
            id_exercise=r["id_exercise"],
            type=typ,  # 'text_question'
            level=r["level"],
            topics=list(r.get("topics") or []),
            text=r["text"],
            image_url=r.get("image_url") or "",
            questions=[
                QuestionDTO(**q) for q in (r.get("questions") or []) if isinstance(q, dict)
            ],
        )


ExerciseBaseDTO = Annotated[
    Union[ExerciseMatchDTO, ExerciseQuestionDTO],
    Field(discriminator="type"),
]
