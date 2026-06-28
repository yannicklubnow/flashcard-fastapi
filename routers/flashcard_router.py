from database.connection import db_dependency
from fastapi import APIRouter
from models.flashcard import FlashcardUpdate, FlashcardInput
from services import flashcard_service

router = APIRouter()


@router.post("/flashcards", status_code=201)
async def create_card_endpoint(card: FlashcardInput, db: db_dependency):
    cursor, connection = db
    return flashcard_service.create_card(card, cursor, connection)


@router.get("/flashcards/category", status_code=200)
async def get_all_categories_endpoint(db: db_dependency):
    cursor, _ = db
    return flashcard_service.get_all_categories_or_404(cursor)


@router.get("/flashcards/category/{category_name}", status_code=200)
async def get_cards_by_category_endpoint(category_name: str, db: db_dependency):
    cursor, _ = db
    return flashcard_service.get_cards_by_category_or_404(category_name, cursor)


@router.delete("/flashcards/category/{category_name}", status_code=200)
async def delete_category_endpoint(category_name: str, db: db_dependency):
    cursor, connection = db
    return flashcard_service.delete_category(category_name, cursor, connection)


@router.get("/flashcards/{card_id}", status_code=200)
async def get_card_by_id_endpoint(card_id: str, db: db_dependency):
    cursor, _ = db
    return flashcard_service.get_card_by_id_or_404(card_id, cursor)


@router.get("/flashcards", status_code=200)
async def get_all_cards_endpoint(db: db_dependency):
    cursor, _ = db
    return flashcard_service.get_all_cards_or_404(cursor)


@router.patch("/flashcards/{card_id}", status_code=200)
async def edit_card_endpoint(
    card_id: str, flashcard: FlashcardUpdate, db: db_dependency
):
    cursor, connection = db
    return flashcard_service.edit_card(card_id, flashcard, cursor, connection)


@router.delete("/flashcards/{card_id}", status_code=200)
async def delete_card_endpoint(card_id: str, db: db_dependency):
    cursor, connection = db
    return flashcard_service.delete_card(card_id, cursor, connection)
