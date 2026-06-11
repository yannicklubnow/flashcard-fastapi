from pydantic import BaseModel

class FlashcardBase(BaseModel):
    category: str | None = None
    question: str | None = None
    answer: str | None = None
    hint: str | None = None

class Flashcard(FlashcardBase):
    category: str
    question: str
    answer: str

class FlashcardUpdate(FlashcardBase):
    pass
