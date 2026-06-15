from fastapi import FastAPI
from routers.flashcard import router as flashcard_router
from routers.session import router as session_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome!"}


app.include_router(flashcard_router)
app.include_router(session_router)
