from database import flashcard_db
from fastapi import APIRouter, HTTPException
from models.flashcard import FlashcardUpdate, FlashcardInput, FlashcardCreate

router = APIRouter()


@router.post("/flashcards", status_code=201)
async def add_card(card: FlashcardInput):
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
    )
    return {"message": f'Flashcard with id "{new_card.id}" added successfully.'}


@router.get("/flashcards/category")
async def get_all_categories():
    categories = flashcard_db.select_all_categories()
    if not categories:
        return {"message": "No categories found."}
    return categories


@router.get("/flashcards/{card_id}")
async def get_card_by_id(card_id: str): 
    card = flashcard_db.select_card_by_id(card_id)
    if not card:
        raise HTTPException(
            status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
        )
    return card


@router.get("/flashcards/category/{category_name}")
async def get_cards_by_category(category_name: str):
    cards = flashcard_db.select_card_by_category(category_name)
    if not cards:
        raise HTTPException(
            status_code=404, detail=f'Category "{category_name}" not found.'
        )
    return cards

@router.get("/flashcards")
async def get_all_cards():
    cards = flashcard_db.select_all_cards()
    if not cards:
        raise HTTPException(status_code=404, detail=f"No flashcards found.")
    return cards


@router.patch("/flashcards/{card_id}")
async def edit_card(card_id: str, flashcard: FlashcardUpdate):
    card = flashcard_db.select_card_by_id(card_id)

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
    )
    return {
        "message": f'Flashcard with id "{card_id}" successfully updated.',
        "card": card,
    }


@router.delete("/flashcards/{card_id}")
async def delete_card(card_id: str):
    card = flashcard_db.select_card_by_id(card_id)
    if not card:
        raise HTTPException(
            status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
        )
    flashcard_db.delete_card(card_id)
    return {"message": f"Flashcard with id {card_id} successfully deleted."}



@router.delete("/flashcards/category/{category_name}")
async def delete_category(category_name: str):
    cards = flashcard_db.select_card_by_category(category_name)
    if not cards:
        raise HTTPException(
            status_code=404,
            detail=f'Flashcard with category "{category_name}" not found.',
        )
    flashcard_db.delete_category(category_name)
    return {"message": f'Category "{category_name}" successfully deleted.'}
