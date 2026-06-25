from database.connection import connection, cursor


def insert_session(session_id: str, number_of_cards: int, categories: list[str]):
    """Inserts a session into the database."""
    cursor.execute(
    '''
    INSERT into
        sessions(id, number_of_cards)
    VALUES(?, ?)
    ''',
        (session_id, number_of_cards),
    )
    for category in categories:
        cursor.execute(
        '''
        INSERT into
            session_categories(session_id, category_name)
        VALUES (?, ?)
        ''',
            (session_id, category),
        )
    connection.commit()


def insert_session_cards(session_id: str, card_id: str):
    """Inserts a flashcard to a session."""
    cursor.execute(
    '''
    INSERT into 
        session_cards(session_id, card_id)
    VALUES (?, ?)
    ''',
        (session_id, card_id),
    )
    connection.commit()


def select_session_by_id(session_id: str):
    """Returns a session by id."""
    cursor.execute(
    '''
    SELECT * 
    FROM sessions 
    WHERE id = ?
    ''',
        (session_id,),
    )
    return cursor.fetchone()
    

def update_status(session_id: str, status: str):
    """Updates the sessions status."""
    cursor.execute(
    '''
    UPDATE sessions
    SET status = ?
    WHERE id = ?
    ''',
        (status, session_id)
    )
    connection.commit()

def update_number_of_cards(session_id: str, number_of_cards: int):
    """Updates the sessions number of selected cards."""
    cursor.execute(
    '''
    UPDATE sessions
    SET number_of_cards = ?
    WHERE id = ?
    ''',
        (number_of_cards, session_id)
    )
    connection.commit()

def select_session_cards(session_id: str):
    """Returns all cards from a session."""
    cursor.execute(
    '''
    SELECT flashcards.* FROM session_cards 
    JOIN flashcards ON session_cards.card_id = flashcards.id
    WHERE session_cards.session_id = ?
    ''',
        (session_id,),
    )
    return cursor.fetchall()


def select_session_cards_by_answer(session_id: str, user_answer: str):
    """Returns cards by answers from a session."""
    cursor.execute(
    '''
    SELECT flashcards.* FROM session_cards 
    JOIN flashcards ON session_cards.card_id = flashcards.id
    WHERE session_cards.session_id = ?
    AND session_cards.user_answer = ?
    ''',
        (session_id, user_answer),
    )
    return cursor.fetchall()


def select_session_card(session_id: str, card_id: str):
    """Returns a card from a session."""
    cursor.execute(
    '''
    SELECT flashcards.* FROM session_cards 
    JOIN flashcards ON session_cards.card_id = flashcards.id
    WHERE session_cards.session_id = ? 
    AND session_cards.card_id = ?
    ''',
        (session_id, card_id),
    )
    return cursor.fetchone()


def select_session_categories(session_id: str):
    """Returns all categories from a session."""
    cursor.execute(
    '''
    SELECT category_name FROM session_categories
    WHERE session_categories.session_id  = ?
    ''',
        (session_id,),
    )
    return cursor.fetchall()


def delete_session(session_id: str):
    """Deletes a session."""
    cursor.execute(
    '''
    DELETE 
    FROM sessions 
    WHERE id = ?
    ''',
        (session_id,),
    )
    connection.commit()


def update_session_card_answer(session_id: str, card_id: str, user_answer: str):
    """Updates a card in a session from unanswered to correct or incorrect."""
    cursor.execute(
    '''
    UPDATE session_cards 
    SET user_answer = ?
    WHERE session_cards.session_id = ? 
    AND session_cards.card_id = ?
    ''',
        (user_answer, session_id, card_id),
    )
    connection.commit()
