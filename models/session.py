import uuid

from pydantic import BaseModel, Field


class SessionInput(BaseModel):
    number_of_cards: int
    categories: list[str] = Field(default_factory=list)


class SessionCreate(SessionInput):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
