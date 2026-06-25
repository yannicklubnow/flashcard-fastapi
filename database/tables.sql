-- Stores all flashcards
CREATE TABLE IF NOT EXISTS flashcards (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    hint TEXT
);


-- Stores all sessions
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    number_of_cards INTEGER NOT NULL,
    status TEXT DEFAULT 'created'
    CHECK (status IN ('created', 'active', 'finished'))
);


-- Links flashcards to a session with answer tracking
CREATE TABLE IF NOT EXISTS session_cards (
    session_id TEXT REFERENCES sessions (id) ON DELETE CASCADE,
    card_id TEXT REFERENCES flashcards (id),
    user_answer TEXT DEFAULT 'unanswered'
    CHECK (user_answer IN ('unanswered', 'correct', 'incorrect'))
);


-- Links categories to a session
CREATE TABLE IF NOT EXISTS session_categories (
    session_id TEXT REFERENCES sessions (id) ON DELETE CASCADE,
    category_name TEXT NOT NULL
);
