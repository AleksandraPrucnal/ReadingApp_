"""Exercise endpoints (airport-style DTOs) — bez autentykacji."""

from typing import Iterable, Sequence
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from src.container import Container
from src.core.domain.enums import ExerciseType
from src.infrastructure.dto.exerciseDTO import (
    ExerciseBaseDTO,
    ExerciseMatchDTO,
    ExerciseQuestionDTO,
    QuestionDTO,
)
from src.core.domain.exercises.exercise_match import ExerciseMatchIn
from src.core.domain.exercises.exercise_question import ExerciseQuestionIn
from src.core.domain.exercises.question import QuestionIn
from src.infrastructure.services.iexercise import IExerciseService

from src.api.deps.auth import get_current_user, CurrentUser

router = APIRouter(prefix="/exercises", tags=["exercises"])

# --------------------------- Answer checking -----------------------------------

class MatchAnswerIn(BaseModel):
    id_exercise: int
    selected_index: int


class MatchAnswerOut(BaseModel):
    id_exercise: int
    is_correct: bool


@router.post("/check/match", response_model=MatchAnswerOut, status_code=200)
@inject
async def check_match_answer(
    body: MatchAnswerIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
    user: CurrentUser = Depends(get_current_user),  
) -> MatchAnswerOut:
    ex_id, ok = await service.check_answer_match(
        id_exercise=body.id_exercise,
        selected_index=body.selected_index,
        user_id=user.id_user,
    )
    return MatchAnswerOut(id_exercise=ex_id, is_correct=ok)


class QuestionAnswerIn(BaseModel):
    id_exercise: int
    id_question: int
    selected_index: int


class QuestionAnswerOut(BaseModel):
    id_exercise: int
    id_question: int
    is_correct: bool


@router.post("/check/question", response_model=QuestionAnswerOut, status_code=200)
@inject
async def check_question_answer(
    body: QuestionAnswerIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
    user: CurrentUser = Depends(get_current_user),
) -> QuestionAnswerOut:
    ex_id, q_id, ok = await service.check_answer_question_single(
        id_exercise=body.id_exercise,
        id_question=body.id_question,
        selected_index=body.selected_index,
        user_id=user.id_user,
    )
    return QuestionAnswerOut(id_exercise=ex_id, id_question=q_id, is_correct=ok)

# --------------------------- Read endpoints ------------------------------------

@router.get("/all", response_model=Iterable[ExerciseBaseDTO], status_code=200)
@inject
async def get_all_exercises(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> Iterable[ExerciseBaseDTO]:
    return await service.get_all_exercises(limit=limit, offset=offset)


@router.get("/{id_exercise}", response_model=ExerciseBaseDTO, status_code=200)
@inject
async def get_exercise_by_id(
    id_exercise: int,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> ExerciseBaseDTO:
    ex = await service.get_by_id(id_exercise)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return ex


@router.get("/type/{ex_type}", response_model=Iterable[ExerciseBaseDTO], status_code=200)
@inject
async def get_exercises_by_type(
    ex_type: ExerciseType,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> Iterable[ExerciseBaseDTO]:
    return await service.get_by_type(ex_type, limit=limit, offset=offset)


@router.get("/level/{level}", response_model=Iterable[ExerciseBaseDTO], status_code=200)
@inject
async def get_exercises_by_level(
    level: int,
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> Iterable[ExerciseBaseDTO]:
    return await service.get_by_level(level, limit=limit, offset=offset)


@router.get("/topics", response_model=Iterable[ExerciseBaseDTO], status_code=200)
@inject
async def get_exercises_by_topics(
    topic_ids: Sequence[int] = Query(..., description="Powtarzalny parametr: ?topic_ids=1&topic_ids=2"),
    match_all: bool = Query(False, description="True=AND (wszystkie), False=OR (dowolny)"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> Iterable[ExerciseBaseDTO]:
    return await service.get_by_topics(topic_ids, match_all=match_all, limit=limit, offset=offset)


# --------------------------- Questions read ------------------------------------

@router.get("/{id_exercise}/questions", response_model=Iterable[QuestionDTO], status_code=200)
@inject
async def list_questions(
    id_exercise: int,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> Iterable[QuestionDTO]:
    return await service.list_questions(id_exercise)


@router.get("/question/{id_question}", response_model=QuestionDTO | None, status_code=200)
@inject
async def get_question(
    id_question: int,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> QuestionDTO | None:
    return await service.get_question(id_question)


# --------------------------- Create endpoints ----------------------------------

@router.post("/match", response_model=ExerciseMatchDTO, status_code=201)
@inject
async def create_match_exercise(
    payload: ExerciseMatchIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> ExerciseMatchDTO | None:
    ex = await service.add_exercise_match(payload)
    if not ex:
        raise HTTPException(status_code=400, detail="Create failed")
    return ex  # type: ignore[return-value]


@router.post("/question", response_model=ExerciseQuestionDTO, status_code=201)
@inject
async def create_question_exercise(
    payload: ExerciseQuestionIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> ExerciseQuestionDTO | None:
    ex = await service.add_exercise_question(payload)
    if not ex:
        raise HTTPException(status_code=400, detail="Create failed")
    return ex  # type: ignore[return-value]


@router.post("/{id_exercise}/question", response_model=QuestionDTO, status_code=201)
@inject
async def add_question_to_exercise(
    id_exercise: int,
    payload: QuestionIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> QuestionDTO | None:
    q = await service.add_question(id_exercise, payload)
    if not q:
        raise HTTPException(status_code=400, detail="Create failed")
    return q


# --------------------------- Update endpoints ----------------------------------

@router.put("/match/{id_exercise}", response_model=ExerciseMatchDTO, status_code=200)
@inject
async def update_match_exercise(
    id_exercise: int,
    payload: ExerciseMatchIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> ExerciseMatchDTO | None:
    ex = await service.update_exercise_match(id_exercise, payload)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found or wrong type")
    return ex  # type: ignore[return-value]


@router.put("/question/{id_exercise}", response_model=ExerciseQuestionDTO, status_code=200)
@inject
async def update_question_exercise(
    id_exercise: int,
    payload: ExerciseQuestionIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> ExerciseQuestionDTO | None:
    ex = await service.update_exercise_question(id_exercise, payload)
    if not ex:
        raise HTTPException(status_code=404, detail="Exercise not found or wrong type")
    return ex  # type: ignore[return-value]


@router.put("/question-item/{id_question}", response_model=QuestionDTO, status_code=200)
@inject
async def update_question_item(
    id_question: int,
    payload: QuestionIn,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> QuestionDTO | None:
    q = await service.update_question(id_question, payload)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q


# --------------------------- Delete endpoints ----------------------------------

@router.delete("/{id_exercise}", status_code=204)
@inject
async def delete_exercise(
    id_exercise: int,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> None:
    ok = await service.delete_exercise(id_exercise)
    if not ok:
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.delete("/question/{id_question}", status_code=204)
@inject
async def delete_question(
    id_question: int,
    service: IExerciseService = Depends(Provide[Container.exercise_service]),
) -> None:
    ok = await service.delete_question(id_question)
    if not ok:
        raise HTTPException(status_code=404, detail="Question not found")
