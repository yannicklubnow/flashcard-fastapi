import sqlite3
import random

from fastapi import HTTPException
from models.session import SessionInput, SessionCreate
from database import flashcard_db, session_db


def get_session_or_404(session_id: str, cursor: sqlite3.Cursor):
    session = session_db.select_session_by_id(session_id, cursor)
    if not session:
        raise HTTPException(
            status_code=404, detail=f'Session with id "{session_id}" not found.'
        )
    return session


def get_card_or_404(card_id: str, cursor: sqlite3.Cursor):
    card = flashcard_db.select_card_by_id(card_id, cursor)
    if not card:
        raise HTTPException(
            status_code=404, detail=f'Card with id "{card_id}" not found.'
        )
    return card


def create_session(
    session: SessionInput, cursor: sqlite3.Cursor, connection: sqlite3.Connection
):
    _validate_categories(session.categories, cursor)

    new_session = SessionCreate(
        number_of_cards=session.number_of_cards, categories=session.categories
    )

    session_db.insert_session(
        new_session.id,
        new_session.number_of_cards,
        new_session.categories,
        cursor,
        connection,
    )

    return {"message": "Session successfully created.", "session": new_session}


def _validate_categories(categories: list[str], cursor: sqlite3.Cursor):
    all_categories = [c["category"] for c in flashcard_db.select_all_categories(cursor)]
    for category in categories:
        if category not in all_categories:
            raise HTTPException(
                status_code=404, detail=f'Category "{category}" not found.'
            )


def add_card_to_session(
    session_id: str,
    card_id: str,
    cursor: sqlite3.Cursor,
    connection: sqlite3.Connection,
):
    get_session_or_404(session_id, cursor)
    get_card_or_404(card_id, cursor)

    session_db.insert_session_cards(session_id, card_id, cursor, connection)

    return {
        "message": f'Flashcard with id "{card_id}" successfully added to the session with id "{session_id}".'
    }


def start_session(
    session_id: str, cursor: sqlite3.Cursor, connection: sqlite3.Connection
):

    session = get_session_or_404(session_id, cursor)

    if session["status"] != "created":
        raise HTTPException(
            status_code=400, detail=f'Session with id: "{session_id}" not created.'
        )

    filtered_cards = _get_filtered_cards(session_id, cursor)
    actual_card_count = _assign_cards_to_session(
        session_id, session["number_of_cards"], filtered_cards, cursor, connection
    )
    session_db.update_status(session_id, "active", cursor, connection)
    session_db.update_number_of_cards(session_id, actual_card_count, cursor, connection)

    updated_session = session_db.select_session_by_id(session_id, cursor)

    return {
        "message": f'Session with id "{session_id}" successfully started.',
        "session": updated_session,
    }


def _get_filtered_cards(session_id: str, cursor: sqlite3.Cursor):
    filtered_cards = []
    categories = session_db.select_session_categories(session_id, cursor)

    for category in categories:
        cards = flashcard_db.select_card_by_category(category["category_name"], cursor)
        filtered_cards.extend(cards)
    return filtered_cards


def _assign_cards_to_session(
    session_id: str,
    number_of_cards: int,
    filtered_cards: list,
    cursor: sqlite3.Cursor,
    connection: sqlite3.Connection,
):
    selected_cards = random.sample(
        filtered_cards, min(len(filtered_cards), number_of_cards)
    )
    for card in selected_cards:
        session_db.insert_session_cards(session_id, card["id"], cursor, connection)

    return len(selected_cards)


def finish_session(
    session_id: str, cursor: sqlite3.Cursor, connection: sqlite3.Connection
):
    get_session_or_404(session_id, cursor)
    session_db.update_status(session_id, "finished", cursor, connection)
    return {
        "message": f'Session with id "{session_id}" successfully finished.',
    }


def delete_session(
    session_id: str, cursor: sqlite3.Cursor, connection: sqlite3.Connection
):
    get_session_or_404(session_id, cursor)
    session_db.delete_session(session_id, cursor, connection)
    return {"message": f'Session with id "{session_id}" successfully deleted'}


def get_cards_of_session(session_id: str, cursor: sqlite3.Cursor):
    get_session_or_404(session_id, cursor)
    cards = session_db.select_session_cards(session_id, cursor)
    if not cards:
        raise HTTPException(
            status_code=404, detail=f'No cards added to session with id "{session_id}".'
        )
    return cards


def update_user_answer(
    session_id: str,
    card_id: str,
    correct_answer: bool,
    cursor: sqlite3.Cursor,
    connection: sqlite3.Connection,
):
    session = get_session_or_404(session_id, cursor)
    _validate_card_in_session(session_id, card_id, cursor)

    answer = "correct" if correct_answer else "incorrect"
    session_db.update_session_card_answer(
        session_id, card_id, answer, cursor, connection
    )

    unanswered_cards = session_db.select_session_cards_by_answer(
        session_id, "unanswered", cursor
    )
    incorrect_cards = session_db.select_session_cards_by_answer(
        session_id, "incorrect", cursor
    )

    if not unanswered_cards and not incorrect_cards:
        return {
            "message": f"Congratulations! You finished a session with {session['number_of_cards']} cards."
        }

    if not unanswered_cards and incorrect_cards:
        _reset_incorrect_cards(session_id, incorrect_cards, cursor, connection)
        return {"message": "Round complete! Incorrect cards will be repeated."}

    correct_cards = session_db.select_session_cards_by_answer(
        session_id, "correct", cursor
    )
    return {
        "message": f"You got {len(correct_cards)}/{session['number_of_cards']} cards correctly."
    }


def _validate_card_in_session(session_id: str, card_id: str, cursor: sqlite3.Cursor):
    session_card = session_db.select_session_card(session_id, card_id, cursor)
    if not session_card:
        raise HTTPException(
            status_code=404, detail=f'Card with id "{card_id}" not found in session.'
        )
    


def _reset_incorrect_cards(session_id: str, incorrect_cards: list, cursor: sqlite3.Cursor, connection: sqlite3.Connection):
    for card in incorrect_cards:
        session_db.update_session_card_answer(
            session_id, card["id"], "unanswered", cursor, connection
        )
