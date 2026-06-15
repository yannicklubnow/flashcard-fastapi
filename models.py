import uuid

from pydantic import BaseModel, Field
from enum import Enum


class FlashcardInput(BaseModel):
    category: str
    question: str
    answer: str
    hint: str | None = None


class Flashcard(FlashcardInput):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class FlashcardUpdate(BaseModel):
    category: str | None = None
    question: str | None = None
    answer: str | None = None
    hint: str | None = None


class SessionStatus(Enum):
    CREATED = "created"
    ACTIVE = "active"
    FINISHED = "finished"


class SessionInput(BaseModel):
    number_of_cards: int
    categories: list[str] = Field(default_factory=list)


class Session(SessionInput):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cards: list[Flashcard] = Field(default_factory=list)
    correct_cards: list[Flashcard] = Field(default_factory=list)
    incorrect_cards: list[Flashcard] = Field(default_factory=list)
    status: SessionStatus = SessionStatus.CREATED
