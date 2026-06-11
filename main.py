import uuid

from fastapi import FastAPI, HTTPException
from models import Flashcard, FlashcardUpdate


app = FastAPI()

flashcards = []


@app.get("/")
async def root():
    return {"message": "this is your flashcard website"}


@app.get("/flashcards")
async def get_cards_by(card_id: str | None = None, category_name: str | None = None):
    if card_id:
        for card in flashcards:
            if card["id"] == card_id:
                return card
        raise HTTPException(status_code=404, detail=f"Flashcard with this id: {card_id} not found.")

    if category_name:
        cards_of_category = [card for card in flashcards if card["category"] == category_name]
        if not cards_of_category:
            raise HTTPException(status_code=404, detail=f"Category {category_name} not found.")
        return cards_of_category

    else: return flashcards


@app.get("/flashcards/category")
async def get_all_categories():
    categories = set(card["category"] for card in flashcards)
    return list(categories)


@app.delete("/flashcards/category/{category_name}")
async def delete_category(category_name: str):
    cards_to_delete = [card for card in flashcards if card["category"] == category_name]
    if not cards_to_delete:
        raise HTTPException(status_code=404, detail=f"Flashcard with category: {category_name} not found.")
    for cards in cards_to_delete:
        flashcards.remove(cards)
    return {"message": f"Category {category_name} successfully deleted."}



@app.post("/flashcards")
async def add_card(card: Flashcard):
    new_card = card.model_dump()
    new_card["id"] = str(uuid.uuid4())
    flashcards.append(new_card)
    return {"message": "Flashcard added successfully."}



@app.delete("/flashcards/{card_id}")
async def delete_card(card_id: str):
    for card in flashcards:
        if card["id"] == card_id:
            flashcards.remove(card)
            return {"message": "Flashcard successfully deleted."}
    raise HTTPException(status_code=404, detail=f"Flashcard with id: {card_id} not found.")


@app.patch("/flashcards/{card_id}")
async def update_card(card_id: str, flashcard: FlashcardUpdate):
    for card in flashcards:
        if card["id"] == card_id:
            card.update(flashcard.model_dump(exclude_unset=True))
            return card
    raise HTTPException(status_code=404, detail=f"Flashcard with id: {card_id} not found")