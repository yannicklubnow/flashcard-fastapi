import uuid

from pydantic import BaseModel, Field


class FlashcardInput(BaseModel):
    category: str
    question: str
    answer: str
    hint: str | None = None


class FlashcardCreate(FlashcardInput):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class FlashcardUpdate(BaseModel):
    category: str | None = None
    question: str | None = None
    answer: str | None = None
    hint: str | None = None
