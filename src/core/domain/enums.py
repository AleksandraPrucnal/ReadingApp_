from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    MENTOR = "mentor"
    MANAGER = "manager"

class ExerciseType(str, Enum):
    MATCH = "match_image"
    QUESTION = "text_question"

class UiMode(str, Enum):
    LIGHT = "light"
    DARK = "dark"