import random

from fastapi import APIRouter, HTTPException
from models import SessionInput, Session, SessionStatus
from database import sessions, flashcards

router = APIRouter()


@router.post("/sessions")
async def create_session(session: SessionInput):
    new_session = Session(
        number_of_cards=session.number_of_cards, categories=session.categories
    )
    sessions.append(new_session)
    return {"message": "Session successfully created.", "session": new_session}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    return _find_session(session_id)


@router.patch("/sessions/{session_id}")
async def start_session(session_id: str):
    session = _find_session(session_id)
    if session.status == SessionStatus.CREATED:

        session.status = SessionStatus.ACTIVE
        filtered_cards = [
            card for card in flashcards if card.category in session.categories
        ]

        session.cards = random.sample(
            filtered_cards, min(len(filtered_cards), session.number_of_cards)
        )

        return {"message": "Session successfully started.", "session": session}
    else:
        raise HTTPException(
            status_code=400, detail=f'Session with id: "{session_id}" not created.'
        )


@router.delete("/sessions/{session_id}")
async def end_session(session_id: str):
    session = _find_session(session_id)
    sessions.remove(session)
    return {
        "message": f'Session with id "{session_id}" sucessfully deleted',
        "session": session,
    }


@router.get("/sessions/{session_id}/cards")
async def get_cards_of_session(session_id: str):
    session = _find_session(session_id)
    return session.cards


@router.patch("/sessions/{session_id}/cards/{card_id}")
async def user_answer(session_id: str, card_id: str, correct_answer: bool):
    session = _find_session(session_id)
    for card in session.cards:
        if card.id == card_id:
            if correct_answer:
                session.correct_cards.append(card)
            else:
                session.incorrect_cards.append(card)
            session.cards.remove(card)

            if not session.cards and session.incorrect_cards:
                session.cards = session.incorrect_cards
                session.incorrect_cards = []

            answered_cards = len(session.correct_cards) + len(session.incorrect_cards)
            total_num_cards = answered_cards + len(session.cards)
            if not session.cards:
                return {
                    "message": f"Congratulations, you finished a session with {total_num_cards} flashcards."
                }
            return {"message": f"You answered {answered_cards}/{total_num_cards}"}

    raise HTTPException(
        status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
    )


def _find_session(session_id: str):
    for session in sessions:
        if session.id == session_id:
            return session
    raise HTTPException(
        status_code=404, detail=f'Session with id "{session_id}" not found.'
    )
