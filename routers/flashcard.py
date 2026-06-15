from fastapi import APIRouter, HTTPException
from models import FlashcardUpdate, Flashcard
from database import flashcards

router = APIRouter()


@router.post("/flashcards")
async def add_card(card: Flashcard):
    flashcards.append(card)
    return {"message": f'Flashcard with id "{Flashcard.id}" added successfully.'}


@router.get("/flashcards")
async def get_cards_by(card_id: str | None = None, category_name: str | None = None):
    if not flashcards:
        return {"message": "No flashcards found."}
    if card_id:
        for card in flashcards:
            if card.id == card_id:
                return card
        raise HTTPException(
            status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
        )

    if category_name:
        cards_of_category = [
            card for card in flashcards if card.category == category_name
        ]
        if not cards_of_category:
            raise HTTPException(
                status_code=404, detail=f'Category "{category_name}" not found.'
            )
        return cards_of_category

    else:
        return flashcards


@router.patch("/flashcards/{card_id}")
async def edit_card(card_id: str, flashcard: FlashcardUpdate):
    for index, card in enumerate(flashcards):
        if card.id == card_id:
            flashcards[index] = card.model_copy(
                update=flashcard.model_dump(exclude_unset=True)
            )
            return {
                "message": f'Flashcard with id "{card_id}" successfully updated.',
                "card": flashcards[index],
            }
    raise HTTPException(
        status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
    )


@router.delete("/flashcards/{card_id}")
async def delete_card(card_id: str):
    for card in flashcards:
        if card.id == card_id:
            flashcards.remove(card)
            return {"message": f"Flashcard with id {card_id} successfully deleted."}
    raise HTTPException(
        status_code=404, detail=f'Flashcard with id "{card_id}" not found.'
    )


@router.get("/flashcards/category")
async def get_all_categories():
    if not flashcards:
        return {"message": "No categories found."}
    all_categories = set(card.category for card in flashcards)
    return list(all_categories)


@router.delete("/flashcards/category/{category_name}")
async def delete_category(category_name: str):
    cards_to_delete = [card for card in flashcards if card.category == category_name]
    if not cards_to_delete:
        raise HTTPException(
            status_code=404,
            detail=f'Flashcard with category "{category_name}" not found.',
        )
    for cards in cards_to_delete:
        flashcards.remove(cards)
    return {"message": f'Category "{category_name}" successfully deleted.'}
