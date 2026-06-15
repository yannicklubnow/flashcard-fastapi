# Flashcard API

![FastAPI](https://img.shields.io/badge/FastAPI-0.136-green)
![Python](https://img.shields.io/badge/Python-3.14-blue)

A REST API for managing flashcards and learning sessions, built with FastAPI and Python.

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
| POST | /sessions | Create a new session |
| GET | /sessions/{id} | Get a session |
| PATCH | /sessions/{id} | Start a session |
| PATCH | /sessions/{id}/cards/{card_id} | Answer a flashcard |
| GET | /sessions/{id}/cards | Get all cards of a session |
| DELETE | /sessions/{id} | Delete a session |

## ✅ Features
- Flashcard management (CRUD)
- Category management
- Learning sessions with random card selection
- Answer tracking with automatic repeat of incorrect cards

## 🔮 Planned (V3)
- Database integration 
- User authentication
- Global card performance tracking
- Web UI