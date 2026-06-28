from fastapi import FastAPI
from routers.flashcard_router import router as flashcard_router
from routers.session_router import router as session_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome!"}


app.include_router(flashcard_router)
app.include_router(session_router)
