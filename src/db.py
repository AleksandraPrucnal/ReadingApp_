import asyncio
import databases
import sqlalchemy
from sqlalchemy.sql import text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB, ARRAY
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    Enum,
    Index,
    UniqueConstraint,
    CheckConstraint,
)
from enum import Enum as PyEnum
from sqlalchemy.exc import OperationalError, DatabaseError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.mutable import MutableList
from asyncpg.exceptions import (
    CannotConnectNowError,
    ConnectionDoesNotExistError,
)
from src.core.domain.enums import UserRole, ExerciseType, UiMode
from src.config import config

from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import ENUM, ARRAY


metadata = sqlalchemy.MetaData()


exercise_type_enum = ENUM(
    ExerciseType,
    name="exercise_type_enum",
    create_type=True,
    native_enum=True,
)

ui_mode_enum = ENUM(
    UiMode,
    name="ui_mode_enum",
    create_type=True,
    native_enum=True,
)

user_table = Table(
    "users",
    metadata,
    Column("id_user", PGUUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")),
    Column("username", String(150), nullable=False, unique=True),
    Column("email", String(320), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column(
        "role",
        SAEnum(
            UserRole,
            name="user_role_enum",
            values_callable=lambda enum_cls: [m.value for m in enum_cls],  # <- kluczowe
        ),
        nullable=False,
        server_default=UserRole.STUDENT.value,  # 'student' – spójne z typem w DB
    ),
    #Column("role", Enum(UserRole, name="user_role_enum"), nullable=False, server_default=UserRole.STUDENT.value),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)


topic_table = Table(
    "topics", metadata,
    Column("id_topic", Integer, primary_key=True, autoincrement=True),
    Column("name", String(200), nullable=False, unique=True),
)


preferences_table = Table(
    "preferences", metadata,
    Column("user_id", PGUUID(as_uuid=True), ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False, index=True),
    Column("favourite_names", ARRAY(String), nullable=False, server_default="{}"),
    Column("family_names", JSONB, nullable=False, server_default=text("'{}'::jsonb")),
    Column(
        "ui_mode",
        SAEnum(
            UiMode,
            name="ui_mode_enum",
            values_callable=lambda enum_cls: [m.value for m in enum_cls],
        ),
        nullable=False,
        server_default=UiMode.LIGHT.value,
    ),
    Column("level", Integer, nullable=False, server_default="1"),
    UniqueConstraint("user_id", name="uq_preferences_user"),
    CheckConstraint("level BETWEEN 1 AND 5", name="ck_preferences_level_1_5"),
)


preferences_topics_table = Table(
    "user_preference_topics", metadata,
    Column("user_id", ForeignKey("preferences.user_id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", ForeignKey("topics.id_topic", ondelete="RESTRICT"), primary_key=True),
)
Index("ix_upt_user", preferences_topics_table.c.user_id)
Index("ix_upt_topic", preferences_topics_table.c.topic_id)


exercise_table = Table(
    "exercises", metadata,
    Column("id_exercise", Integer, primary_key=True, autoincrement=True),
    Column("type", exercise_type_enum, nullable=False),
    Column("level", Integer, nullable=False, index=True),
    Column("topics", ARRAY(Integer), nullable=False, server_default="{}"),  # <-- NOWE
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)


exercise_match_table = Table(
    "exercise_match",metadata,
    Column("exercise_id", ForeignKey("exercises.id_exercise", ondelete="CASCADE"), primary_key=True),
    Column("text", Text, nullable=False),
    Column("image_urls", ARRAY(String), nullable=False, server_default="{}"),  # lista URL-i
    Column("correct_index", Integer, nullable=False),
    CheckConstraint("correct_index >= 0", name="ck_match_correct_index_nonneg"),
)


exercise_question_table = Table(
    "exercise_question",metadata,
    Column("exercise_id", ForeignKey("exercises.id_exercise", ondelete="CASCADE"), primary_key=True),
    Column("text", Text, nullable=False),
    Column("image_url", String(1000), nullable=False),
)


question_table = Table(
    "questions", metadata,
    Column("id_question", Integer, primary_key=True, autoincrement=True),
    Column("exercise_id", ForeignKey("exercises.id_exercise", ondelete="CASCADE"), nullable=False),
    Column("question", Text, nullable=False),
    Column("answers", ARRAY(String), nullable=False),
    Column("correct_index", Integer, nullable=False),
    CheckConstraint("correct_index >= 0", name="ck_question_correct_index_nonneg"),
)
Index("ix_questions_exercise_correct", question_table.c.exercise_id, question_table.c.correct_index)


progress_table = Table(
    "progress",metadata,
    Column("id_event", Integer, primary_key=True, autoincrement=True),
    Column("user_id", PGUUID(as_uuid=True), ForeignKey("users.id_user", ondelete="CASCADE"),
           nullable=False, index=True),
    Column("exercise_id", Integer, ForeignKey("exercises.id_exercise", ondelete="CASCADE"),
           nullable=False, index=True),
    Column("rate", Integer, nullable=False),
    Column("completed_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)
Index("ix_progress_user_exercise", progress_table.c.user_id, progress_table.c.exercise_id)


db_uri = (
    f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}"
    f"@{config.DB_HOST}/{config.DB_NAME}"
)

engine = create_async_engine(
    db_uri,
    echo=True,
    future=True,
    pool_pre_ping=True,
)

database = databases.Database(
    db_uri,
    force_rollback=True,
)


async def run_sql_file(file_path: str):
    with open(file_path, "r") as file:
        statements = file.read().split(";")
    async with engine.begin() as conn:
        for statement in statements:
            if statement.strip():
                await conn.execute(text(statement.strip()))


async def init_db(retries: int = 5, delay: int = 5) -> None:
    for attempt in range(retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(metadata.create_all)
            await run_sql_file("./src/data.sql")
            return
        except (
            OperationalError,
            DatabaseError,
            CannotConnectNowError,
            ConnectionDoesNotExistError,
        ) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(delay)

    raise ConnectionError("Could not connect to DB after several retries.")
