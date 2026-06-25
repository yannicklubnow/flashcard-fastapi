import random

from fastapi import APIRouter, HTTPException
from models.session import SessionInput, SessionCreate
from database import flashcard_db
from database import session_db

router = APIRouter()


@router.post("/sessions", status_code=201)
async def create_session(session: SessionInput):
    all_categories = [c["category"] for c in flashcard_db.select_all_categories()]
    for category in session.categories:
        if category not in all_categories:
            raise HTTPException(
                status_code=404, detail=f'Category "{category}" not found.'
            )

    new_session = SessionCreate(
        number_of_cards=session.number_of_cards, categories=session.categories
    )

    session_db.insert_session(
        new_session.id, new_session.number_of_cards, new_session.categories
    )

    return {"message": "Session successfully created.", "session": new_session}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    return _find_session(session_id)


@router.patch("/sessions/{session_id}")
async def start_session(session_id: str):

    session = _find_session(session_id)

    if session["status"] == "created":
        filtered_cards = []
        categories = session_db.select_session_categories(session_id)

        for category in categories:
            cards = flashcard_db.select_card_by_category(category["category_name"])
            filtered_cards.extend(cards)

        selected_cards = random.sample(
            filtered_cards, min(len(filtered_cards), session["number_of_cards"])
        )
        for card in selected_cards:
            session_db.insert_session_cards(session_id, card["id"])

        session_db.update_status(session_id, "active")
        session_db.update_number_of_cards(session_id, len(selected_cards))

        updated_session = session_db.select_session_by_id(session_id)

        return {
            "message": f'Session with id "{session_id}" successfully started.',
            "session": updated_session,
        }
    else:
        raise HTTPException(
            status_code=400, detail=f'Session with id: "{session_id}" not created.'
        )


@router.patch("/sessions/{session_id}/finish")
async def end_session(session_id: str):
    _find_session(session_id)
    session_db.update_status(session_id, "finished")
    return {
        "message": f'Session with id "{session_id}" successfully finished.',
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    session = _find_session(session_id)
    session_db.delete_session(session_id)
    return {
        "message": f'Session with id "{session_id}" successfully deleted',
        "session": session,
    }


@router.get("/sessions/{session_id}/cards")
async def get_cards_of_session(session_id: str):
    _find_session(session_id)
    cards = session_db.select_session_cards(session_id)
    if not cards:
        return {
            "message": f'No cards added to session with id "{session_id}"',
        }
    return cards


@router.patch("/sessions/{session_id}/cards/{card_id}")
async def user_answer(session_id: str, card_id: str, correct_answer: bool):

    session = _find_session(session_id)
    session_card = session_db.select_session_card(session_id, card_id)

    if not session_card:
        raise HTTPException(
            status_code=404, detail=f'Card with id "{card_id}" not found in session.'
        )
    # Update card answer
    if correct_answer:
        session_db.update_session_card_answer(session_id, card_id, "correct")
    else:
        session_db.update_session_card_answer(session_id, card_id, "incorrect")

    unanswered_cards = session_db.select_session_cards_by_answer(
        session_id, "unanswered"
    )
    incorrect_cards = session_db.select_session_cards_by_answer(session_id, "incorrect")

    if incorrect_cards and not unanswered_cards:
        for card in incorrect_cards:
            session_db.update_session_card_answer(session_id, card["id"], "unanswered")
        return {"message": "Round complete! Incorrect cards will be repeated."}

    total_cards = session["number_of_cards"]
    correct_cards = session_db.select_session_cards_by_answer(session_id, "correct")
    answered_cards = len(correct_cards)

    if not unanswered_cards and not incorrect_cards:
        return {
            "message": f"Congratulations you finished a session with {total_cards} cards."
        }

    return {"message": f"You got {answered_cards}/{total_cards} cards correctly."}


def _find_session(session_id: str):
    session = session_db.select_session_by_id(session_id)
    if not session:
        raise HTTPException(
            status_code=404, detail=f'Session with id "{session_id}" not found.'
        )
    return session
