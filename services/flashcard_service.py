import sqlite3

from database import flashcard_db
from fastapi import HTTPException
from models.flashcard import FlashcardUpdate, FlashcardInput, FlashcardCreate


def create_card(
    card: FlashcardInput, cursor: sqlite3.Cursor, connection: sqlite3.Connection
):
    new_card = FlashcardCreate(
        category=card.category,
        question=card.question,
        answer=card.answer,
        hint=card.hint,
    )

    flashcard_db.insert_card(
        new_card.id,
        new_card.category,
        new_card.question,
        new_card.answer,
        new_card.hint,
        cursor,
        connection,
    )
    return {"message": f'Flashcard with id "{new_card.id}" added successfully.'}


def get_all_categories_or_404(cursor: sqlite3.Cursor):
    categories = flashcard_db.select_all_categories(cursor)
    if not categories:
        raise HTTPException(status_code=404, detail="No categories found.")
    return categories


def get_card_by_id_or_404(card_id: str, cursor: sqlite3.Cursor):
    card = flashcard_db.select_card_by_id(card_id, cursor)
    if not card:
        raise HTTPException(
            status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
        )
    return card


def get_cards_by_category_or_404(category_name: str, cursor: sqlite3.Cursor):
    cards = flashcard_db.select_card_by_category(category_name, cursor)
    if not cards:
        raise HTTPException(
            status_code=404, detail=f'Category "{category_name}" not found.'
        )
    return cards


def get_all_cards_or_404(cursor: sqlite3.Cursor):
    cards = flashcard_db.select_all_cards(cursor)
    if not cards:
        raise HTTPException(status_code=404, detail="No flashcards found.")
    return cards


def edit_card(
    card_id: str,
    flashcard: FlashcardUpdate,
    cursor: sqlite3.Cursor,
    connection: sqlite3.Connection,
):
    card = flashcard_db.select_card_by_id(card_id, cursor)

    if not card:
        raise HTTPException(
            status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
        )
    card = flashcard_db.update_card(
        flashcard.category,
        flashcard.question,
        flashcard.answer,
        flashcard.hint,
        card_id,
        cursor,
        connection,
    )
    return {
        "message": f'Flashcard with id "{card_id}" successfully updated.',
        "card": card,
    }


def delete_card(card_id: str, cursor: sqlite3.Cursor, connection: sqlite3.Connection):
    card = flashcard_db.select_card_by_id(card_id, cursor)
    if not card:
        raise HTTPException(
            status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
        )
    flashcard_db.delete_card(card_id, cursor, connection)
    return {"message": f"Flashcard with id {card_id} successfully deleted."}


def delete_category(
    category_name: str, cursor: sqlite3.Cursor, connection: sqlite3.Connection
):
    cards = flashcard_db.select_card_by_category(category_name, cursor)
    if not cards:
        raise HTTPException(
            status_code=404,
            detail=f'Flashcard with category "{category_name}" not found.',
        )
    flashcard_db.delete_category(category_name, cursor, connection)
    return {"message": f'Category "{category_name}" successfully deleted.'}
