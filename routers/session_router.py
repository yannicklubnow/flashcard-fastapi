from fastapi import APIRouter
from models.session import SessionInput
from database.connection import db_dependency

from services import session_service

router = APIRouter()


@router.post("/sessions", status_code=201) 
async def create_session_endpoint(session: SessionInput, db: db_dependency):
    cursor, connection = db
    return session_service.create_session(session, cursor, connection)


@router.post("/sessions/{session_id}/cards", status_code=201)
async def add_card_to_session_endpoint(
    session_id: str, card_id: str, db: db_dependency
):
    cursor, connection = db
    return session_service.add_card_to_session(session_id, card_id, cursor, connection)


@router.get("/sessions/{session_id}", status_code=200)
async def get_session_endpoint(session_id: str, db: db_dependency):
    cursor, _ = db
    return session_service.get_session_or_404(session_id, cursor)


@router.patch("/sessions/{session_id}", status_code=200)
async def start_session_endpoint(session_id: str, db: db_dependency):
    cursor, connection = db
    return session_service.start_session(session_id, cursor, connection)


@router.patch("/sessions/{session_id}/finish", status_code=200)
async def finish_session_endpoint(session_id: str, db: db_dependency):
    cursor, connection = db
    return session_service.finish_session(session_id, cursor, connection)


@router.delete("/sessions/{session_id}", status_code=200)
async def delete_session_endpoint(session_id: str, db: db_dependency):
    cursor, connection = db
    return session_service.delete_session(session_id, cursor, connection)


@router.get("/sessions/{session_id}/cards", status_code=200)
async def get_cards_of_session_endpoint(session_id: str, db: db_dependency):
    cursor, _ = db
    return session_service.get_cards_of_session(session_id, cursor)


@router.patch("/sessions/{session_id}/cards/{card_id}", status_code=200)
async def user_answer_endpoint(
    session_id: str, card_id: str, correct_answer: bool, db: db_dependency
):
    cursor, connection = db
    return session_service.update_user_answer(
        session_id, card_id, correct_answer, cursor, connection
    )
