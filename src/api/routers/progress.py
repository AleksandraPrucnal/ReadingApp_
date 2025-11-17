# src/api/routers/progress.py
from typing import Iterable
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api.deps.auth import get_current_user, CurrentUser
from src.db import database, progress_table
from sqlalchemy import select

router = APIRouter(prefix="/progress", tags=["progress"])

class ProgressOut(BaseModel):
    id_event: int
    exercise_id: int
    rate: int
    completed_at: str

@router.get("/me", response_model=Iterable[ProgressOut])
async def my_progress(user: CurrentUser = Depends(get_current_user)):
    rows = await database.fetch_all(
        select(
            progress_table.c.id_event,
            progress_table.c.exercise_id,
            progress_table.c.rate,
            progress_table.c.completed_at,
        ).where(progress_table.c.user_id == user.id_user)
         .order_by(progress_table.c.completed_at.desc())
    )
    return [dict(r) for r in rows]
