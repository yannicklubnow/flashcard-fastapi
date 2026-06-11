# Flashcard API

![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![Python](https://img.shields.io/badge/Python-3.14-blue)


A REST API for managing flashcards and categories, built with FastAPI and Python. 

## 🚀 Getting Started

**Prerequisites:** Python 3.10+

```bash
git clone https://github.com/yannicklubnow/flashcard-fastapi.git
cd flashcard-fastapi
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev main.py
```

Then visit **http://127.0.0.1:8000/docs** for the interactive API documentation.


## 🔖 Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /flashcards | Get all flashcards |
| GET | /flashcards?card_id={id} | Get flashcard by ID |
| GET | /flashcards?category_name={name} | Get flashcards by category |
| GET | /flashcards/category | Get all categories |
| POST | /flashcards | Add a new flashcard |
| PATCH | /flashcards/{id} | Update a flashcard |
| DELETE | /flashcards/{id} | Delete a flashcard |
| DELETE | /flashcards/category/{name} | Delete a category |

## 🔮 Planned Features (V2)
- Database integration with SQLite
- User authentication 
- Customizable learning sessions 
- Score tracking and leaderboard